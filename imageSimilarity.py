import monkeymagic
import gevent
from bottle import run, post, request
from sys import path
from skimage.metrics import structural_similarity as ssim
import cv2
import os
import shutil
import argparse
from pyfiglet import Figlet
import hashlib
import numpy as np
import cv2
import logging
import sys
import traceback
import bottle


defaultImagesPath = 'images'
defaultOutputPath = 'output'
defaultSimilarityGrade = 0.95


def log_exceptions(type, value, tb):
    for line in traceback.TracebackException(type, value, tb).format(chain=True):
        logging.exception(line)
    logging.exception(value)

    sys.__excepthook__(type, value, tb)

sys.excepthook = log_exceptions
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024


class Image:
    @classmethod
    def fromPath(cls, path):
        return cls(path, None)

    @classmethod
    def allFromPath(cls, path):
        logging.debug("Reading all images from " + path)
        arrayOfImagesNames = os.listdir(path)
        logging.debug("Files detected: " + str(len(arrayOfImagesNames)))
        arrayOfImages = []

        for imageName in arrayOfImagesNames:
            currentImage = cls.fromPath(path + '/' + imageName)
            arrayOfImages.append(currentImage)

        path == arrayOfImages
        logging.debug("All images read")
        return arrayOfImages

    @classmethod
    def fromBuffer(cls, buffer):
        return cls(None, buffer)

    @classmethod
    def allFromBuffers(cls, buffers):
        arrayOfImages = []

        for buffer in buffers:
            arrayOfImages.append(Image.fromBuffer(buffer))

        return arrayOfImages

    def __init__(self, path=None, buffer=None):
        if path is not None:
            self.imageAsNumpyArray = cv2.imread(path)
            self.name = path.split("/")[-1]
            file = open(path, 'rb')
            self.buffer = file.read()
            file.close()
        elif buffer is not None:
            file_bytes = np.asarray(bytearray(buffer), dtype=np.uint8)
            self.imageAsNumpyArray = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            self.name = ""
            self.buffer = buffer

    def similarityWith(self, anImage):
        selfImageProccessed = cv2.cvtColor(self.imageAsNumpyArray, cv2.COLOR_BGR2GRAY)
        anImageProccessed = cv2.cvtColor(anImage.imageAsNumpyArray, cv2.COLOR_BGR2GRAY)
        similarity = ssim(selfImageProccessed, anImageProccessed)
        return similarity

    def isSimilarWith(self, anImage, minimumSimilarity):
        return self.similarityWith(anImage) >= minimumSimilarity

    def hash(self):
        return hash(self.imageAsNumpyArray.tobytes())

    def sha1(self):
        hasher = hashlib.sha1()
        hasher.update(self.buffer)
        return hasher.hexdigest()


def remove(array, arrays):

    try:
        index = [a.hash() for a in arrays].index(array.hash())
    except ValueError as e:
        print(f'Array not in list. Leaving input unchanged.')
    else:
        arrays.pop(index)


def isImageInsideImages(image, imagesArray):
    return image.hash() in [a.hash() for a in imagesArray]


def hashBuffer(aBuffer):
    hasher = hashlib.sha1()
    hasher.update(aBuffer)
    return hasher.hexdigest()


def saveImagesInLists(listsOfImages, path):
    logging.debug("Saving divisions in {}".format(path))
    try:
        os.mkdir(path)
    except FileExistsError as error:
        shutil.rmtree(path)
        os.mkdir(path)

    for numberOfList in range(0, len(listsOfImages)):
        os.mkdir(path + '/' + str(numberOfList))
        for numberOfImage in range(0, len(listsOfImages[numberOfList])):
            image = listsOfImages[numberOfList][numberOfImage]
            cv2.imwrite(path + '/' + str(numberOfList) + '/' + image.name, image.imageAsNumpyArray)


def printBanner():
    customFiglet = Figlet(font='doom')
    asciiBanner = customFiglet.renderText('Image Similarity')
    print(asciiBanner)


def similarImagesDividedInLists(images, minimumSimilarity):
    lists = []
    wasAdded = False
    logging.debug("Dividing images according to their similarity")
    logging.debug("Number of images to divide: {}".format(len(images)))
    logging.debug("Minimum Similarity: {}".format(len(images)))

    for image in images:

        listOfImagesIndex = 0
        while(listOfImagesIndex < len(lists)):
            if(lists[listOfImagesIndex][0].isSimilarWith(image, minimumSimilarity)):
                lists[listOfImagesIndex].append(image)
                wasAdded = True
                break

            listOfImagesIndex += 1

        if not wasAdded:
            lists.append([image])

        wasAdded = False

    logging.debug("Number of divisions: {}".format(len(lists)))

    return lists


def isValidSimilarityGrade(aSimilarityGrade):
    return 0 <= aSimilarityGrade <= 1


def isValidDirectoryPath(pathString):
    return os.path.isdir(pathString)


def validateDirectoryPath(aSimilarityGrade):
    if not isValidDirectoryPath(aSimilarityGrade):
        print("ERROR: Paths given should exist")
        exit()


def validateSimilarityGrade(directoryPath):
    if not isValidSimilarityGrade(directoryPath):
        print("ERROR: Similarity grade should be between 0 and 1.")
        exit()


def processArguments():
    processedOptions = {}
    parser = argparse.ArgumentParser()
    parser.add_argument('--similarityGrade', '-s', type=float, help="Value between 0 and 1. Default: 0.95")
    parser.add_argument('--imagesDirectory', '-i', help="Path where images are found. Default: 'images' ")
    parser.add_argument('--outputDirectory', '-o', help="Path where processed images are. Default: 'output'")
    parser.add_argument('--runServer', '-r', help="Run server with API.", action='store_true')
    parser.add_argument('--logging', '-l', help="Run server with API.", action='store_true')
    args = parser.parse_args()

    if(args.similarityGrade is not None):
        validateSimilarityGrade(args.similarityGrade)
        processedOptions["similarityGrade"] = args.similarityGrade
    else:
        processedOptions["similarityGrade"] = defaultSimilarityGrade

    if(args.imagesDirectory is not None):
        validateDirectoryPath(args.imagesDirectory)
        processedOptions["imagesPath"] = args.imagesDirectory
    else:
        processedOptions["imagesPath"] = defaultImagesPath

    if(args.outputDirectory is not None):
        processedOptions["outputDirectory"] = args.outputDirectory
    else:
        processedOptions["outputDirectory"] = defaultOutputPath

    processedOptions["logging"] = args.logging
    processedOptions["runServer"] = args.runServer

    return processedOptions


def filesBuffersFromRequest(request):
    logging.debug("Getting buffers from request...")
    filesAsFileUpload = list(request.files.values())
    files = []

    for fileUpload in filesAsFileUpload:
        files.append(fileUpload.file.read())
        logging.debug("File Size: {} bytes".format(len(files[-1])))

    logging.debug("All buffers obtained...")
    return files


def buffersToImages(buffers):
    images = []

    for buffer in buffers:
        images.append(Image.fromBuffer(buffer))

    return images


def hashListsOfImages(lists):
    hashList = []

    for list in lists:
        hashList.append(hashListOfImages(list))

    return hashList


def hashListOfImages(list):
    hashList = []

    for image in list:
        hashList.append(image.sha1())

    return hashList


@post('/api/imageSimilarityByHash')
def imageSimilarityByHash():
    logging.debug("Processing Request..")
    if('similarity_grade' in request.params.keys()):
        similarityGrade = float(request.params['similarity_grade'])

        if not isValidSimilarityGrade(similarityGrade):
            return "ERROR: Similarity grade should be between 0 and 1."

    else:
        similarityGrade = 0.95

    similarityGrade = 0.95
    imagesBuffers = filesBuffersFromRequest(request)
    images = Image.allFromBuffers(imagesBuffers)
    lists = similarImagesDividedInLists(images, float(similarityGrade))
    listsHashListResult = hashListsOfImages(lists)

    return {"lists": listsHashListResult}


def runServer():
    logging.debug("Running server...")
    run(host='0.0.0.0', port=9081, debug=False, server='gevent')
    logging.debug("Server Working...")


def main():

    printBanner()
    optionsProcessed = processArguments()

    if not optionsProcessed["logging"]:
        logging.disable()
    else:
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s] %(message)s', filename='imageSimilarity.log')

    if optionsProcessed["runServer"]:
        runServer()
    else:
        print("Loading images from '{}'...".format(optionsProcessed["imagesPath"]))
        images = Image.allFromPath(optionsProcessed["imagesPath"])
        print("Dividing images in lists according to similarity ({})...".format(optionsProcessed["similarityGrade"]))
        lists = similarImagesDividedInLists(images, optionsProcessed["similarityGrade"])
        print("Saving images in '{}'...".format(optionsProcessed["outputDirectory"]))
        saveImagesInLists(lists, optionsProcessed["outputDirectory"])
    print("Done.")

if __name__ == "__main__":
    main()
