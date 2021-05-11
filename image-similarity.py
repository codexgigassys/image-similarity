#!
from sys import path
from numpy import integer
from skimage.metrics import structural_similarity as ssim
import cv2
import os
import shutil
import argparse
from pyfiglet import Figlet

defaultImagesPath = 'images'
defaultOutputPath = 'output'
defaultSimilarityGrade = 0.95

def isImageInsideImages(image,imagesArray):
    return any((image == x).all() for x in imagesArray)

def saveBatchOfImages(batchsOfImages, path):
    try:
        os.mkdir(path)
    except FileExistsError as error:
        shutil.rmtree(path)
        os.mkdir(path)
    
    for numberOfBatch in range(0,len(batchsOfImages)):
        os.mkdir(path+'/'+str(numberOfBatch))
        for numberOfImage in range(0,len(batchsOfImages[numberOfBatch])):
            image = batchsOfImages[numberOfBatch][numberOfImage]
            cv2.imwrite(path+'/'+str(numberOfBatch)+'/'+str(numberOfImage)+'.jpeg',image)

def printBanner():
    customFiglet = Figlet(font='doom')
    asciiBanner = customFiglet.renderText('Image Similarity')
    print(asciiBanner)

def similarImagesDividedInBatchs(images, minimumSimilarity):
    batchs = []
    imagesCopy = images.copy()
    imagesAlreadyDivided = []

    for image in imagesCopy:
        if len(imagesAlreadyDivided) == 0 or not isImageInsideImages(image,imagesAlreadyDivided):
            similarImages = similarImagesOfImage(image,images,minimumSimilarity)

            for i in similarImages:
                imagesAlreadyDivided.append(i)

            batchs.append(similarImages)
    return batchs

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
    args = parser.parse_args()

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

    return (similarityGrade,imagesPath,outputDirectory)

def main():
    
    printBanner()
    
    (similarityGrade, imagesPath, outputPath) = processArguments()
    print("Loading images from '{}'...".format(imagesPath))
    images = imagesInPath(imagesPath)
    print("Dividing images in batches according to similarity ({})...".format(similarityGrade))
    batchs = similarImagesDividedInBatchs(images,similarityGrade)
    print("Saving images in '{}'...".format(outputPath))
    saveBatchOfImages(batchs,outputPath)
    print("Done.")

    return

if __name__ == "__main__":
    main()