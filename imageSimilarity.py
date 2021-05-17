#!
import monkeymagic
import gevent
from bottle import run,post,request
from sys import path
from numpy import integer
from skimage.metrics import structural_similarity as ssim
import cv2
import os
import shutil
import argparse
from pyfiglet import Figlet
import hashlib
import numpy as np

defaultImagesPath = 'images'
defaultOutputPath = 'output'
defaultSimilarityGrade = 0.95

def isImageInsideImages(image,imagesArray):
    return any((image == x).all() for x in imagesArray)

def hashBuffer(aBuffer):
    hasher = hashlib.sha1()
    hasher.update(aBuffer)
    return  hasher.hexdigest()

def saveImagesInLists(listsOfImages, path):
    try:
        os.mkdir(path)
    except FileExistsError as error:
        shutil.rmtree(path)
        os.mkdir(path)
    
    for numberOfList in range(0,len(listsOfImages)):
        os.mkdir(path+'/'+str(numberOfList))
        for numberOfImage in range(0,len(listsOfImages[numberOfList])):
            image = listsOfImages[numberOfList][numberOfImage]
            cv2.imwrite(path+'/'+str(numberOfList)+'/'+str(numberOfImage)+'.jpeg',image)

def printBanner():
    customFiglet = Figlet(font='doom')
    asciiBanner = customFiglet.renderText('Image Similarity')
    print(asciiBanner)

def similarImagesDividedInLists(images, minimumSimilarity):
    lists = []
    imagesCopy = images.copy()
    imagesAlreadyDivided = []

    for image in imagesCopy:
        if len(imagesAlreadyDivided) == 0 or not isImageInsideImages(image,imagesAlreadyDivided):
            similarImages = similarImagesOfImage(image,images,minimumSimilarity)

            for i in similarImages:
                imagesAlreadyDivided.append(i)

            lists.append(similarImages)
    return lists

def measureSimilarityGradeBetweenImages(imageOne,imageTwo):
    imageOne = cv2.cvtColor(imageOne, cv2.COLOR_BGR2GRAY)
    imageTwo = cv2.cvtColor(imageTwo, cv2.COLOR_BGR2GRAY)
    return ssim(imageOne,imageTwo)

def similarImagesOfImage(image, arrayOfImages, minimumSimilarity):
    similarImages = []
    for anImage in arrayOfImages:
        if measureSimilarityGradeBetweenImages(anImage,image) >= minimumSimilarity:
            similarImages.append(anImage)
    return similarImages

def imagesInPath(imagesPath):
    arrayOfImagesNames = os.listdir(imagesPath)
    arrayOfImages = []

    for imageName in arrayOfImagesNames:
        currentImage = cv2.imread(imagesPath+'/'+imageName)
        arrayOfImages.append(currentImage)
    
    imagesPath == arrayOfImages
    return arrayOfImages

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--similarityGrade', '-s', type=float, help="Value between 0 and 1. Default: 0.95")
    parser.add_argument('--imagesDirectory', '-i', help="Path where images are found. Default: 'images' ")
    parser.add_argument('--outputDirectory', '-o', help="Path where processed images are. Default: 'output'")
    parser.add_argument('--runServer', '-r', help="Run server with API.", action='store_true')
    args = parser.parse_args()

    runServerOption = args.runServer

    if(args.similarityGrade is not None):
        validateSimilarityGrade(args.similarityGrade)
        similarityGrade = args.similarityGrade
    else:
        similarityGrade = defaultSimilarityGrade

    if(args.imagesDirectory is not None):
        validateDirectoryPath(args.imagesDirectory)
        imagesPath = args.imagesDirectory
    else:
        imagesPath = defaultImagesPath

    if(args.outputDirectory is not None):
        outputDirectory = args.outputDirectory
    else:
        outputDirectory = defaultOutputPath

    return (similarityGrade,imagesPath,outputDirectory,runServerOption)

def filesBuffersFromRequest(request):

    filesAsFileUpload = list(request.files.values())
    files = []

    for fileUpload in filesAsFileUpload:
        files.append(fileUpload.file.read())

    return files

def buffersToImages(buffers):
    images = []

    for buffer in buffers:
        images.append(bufferToImage(buffer))

    return images

def bufferToImage(buffer):
    file_bytes = np.asarray(bytearray(buffer), dtype=np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

def imagesHashesDictionaryByFile(imagesBuffers):
    hashDictionary = {}

    for imageBuffer in imagesBuffers:
        hashDictionary[bufferToImage(imageBuffer).tobytes()] = hashBuffer(imageBuffer)
    
    return hashDictionary

def hashListsOfImages(imageHashesDictionary,lists):

    hashList = []

    for list in lists:
        hashList.append(hashListOfImages(imageHashesDictionary, list))

    return hashList

def hashListOfImages(imageHashesDictionary,list):
    hashList = []

    for image in list:
        hashList.append(imageHashesDictionary[image.tobytes()])

    return hashList

@post('/api/imageSimilarityByHash')
def imageSimilarityByHash():
    if( 'similarity_grade' in request.params.keys() ):
        similarityGrade = float(request.params['similarity_grade'])

        if not isValidSimilarityGrade(similarityGrade):
            return "ERROR: Similarity grade should be between 0 and 1."
    
    else:
        similarityGrade = 0.95

    similarityGrade = 0.95
    imagesBuffers = filesBuffersFromRequest(request)
    images = buffersToImages(imagesBuffers)
    lists = similarImagesDividedInLists(images,float(similarityGrade))
    imagesHashesDictionary = imagesHashesDictionaryByFile(imagesBuffers)
    listsHashListResult = hashListsOfImages(imagesHashesDictionary,lists)

    return {"lists":listsHashListResult}

def runServer():
    run(host='0.0.0.0', port=9081, debug=False, server='gevent')

def main():
    
    printBanner()
    
    (similarityGrade, imagesPath, outputPath,runServerOption) = processArguments()

    if runServerOption == True :
        runServer()
    else:
        print("Loading images from '{}'...".format(imagesPath))
        images = imagesInPath(imagesPath)
        print("Dividing images in lists according to similarity ({})...".format(similarityGrade))
        lists = similarImagesDividedInLists(images,similarityGrade)
        print("Saving images in '{}'...".format(outputPath))
        saveImagesInLists(lists,outputPath)
    
    print("Done.")

if __name__ == "__main__":
    main()
