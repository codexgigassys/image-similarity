import sys
import cv2
#The following line is done to get the imageSimilarity.py that is in the previous folder.
sys.path.append('../')
import imageSimilarity
from imageSimilarity import Image

testImages = Image.allFromPath('testImages')

def test_twoEqualImagesHasSimilarityOne():

    imageOne = Image.fromPath('testImages/01.jpeg')
    imageTwo = Image.fromPath('testImages/01.jpeg')

    result = imageOne.similarityWith(imageTwo)

    assert result == 1

def test_twoNotSimilarImagesHasLowSimilarity():
    imageOne = Image.fromPath('testImages/01.jpeg')
    imageTwo = Image.fromPath('testImages/03.jpeg')

    result = imageOne.similarityWith(imageTwo)

    assert result < 0.25

def test_twoSimilarImagesHasHighSimilarity():
    imageOne = Image.fromPath('testImages/01.jpeg')
    imageTwo = Image.fromPath('testImages/02.jpeg')

    result = imageOne.similarityWith(imageTwo)

    assert result > 0.9

def test_imageHasItselfAsSimilarImage():
    image = Image.fromPath('testImages/16.jpeg')
    similarImages = imageSimilarity.similarImagesOfImage(image,testImages,0.95)

    assert imageSimilarity.isImageInsideImages(image,similarImages)

def test_imageHasSomeSimilarImages():
    image = Image.fromPath('testImages/08.jpeg')
    similarImages = imageSimilarity.similarImagesOfImage(image,testImages,0.95)
    quantityOfSimilarImages = len(similarImages)

    assert quantityOfSimilarImages == 14

def test_imageHasOnlyOneImageWithSimilarityOne():
    image = Image.fromPath('testImages/18.jpeg')
    similarImages = imageSimilarity.similarImagesOfImage(image,testImages, 1)
    quantityOfSimilarImages = len(similarImages)

    assert quantityOfSimilarImages == 1

def test_imageTwoDifferentSimilarImagesHasTheSameSimilarImages():
    imageOne = Image.fromPath('testImages/02.jpeg')
    imageTwo = Image.fromPath('testImages/14.jpeg')

    similarImagesOfImageOne = imageSimilarity.similarImagesOfImage(imageOne,testImages,0.95)
    similarImagesOfImageTwo = imageSimilarity.similarImagesOfImage(imageTwo,testImages,0.95)
    quantityOfSimilarImagesOfImageOne = len(similarImagesOfImageOne)
    quantityOfSimilarImagesOfImageTwo = len(similarImagesOfImageTwo)

    assert quantityOfSimilarImagesOfImageOne == quantityOfSimilarImagesOfImageTwo

def test_fiveBatchsFromTestImagesWithHighSimilarity():
    batchs = imageSimilarity.similarImagesDividedInLists(testImages,0.95)
    quantityOfBatchs = len(batchs)
    assert quantityOfBatchs == 5

def test_twentyOneBatchsFromTestImagesWithSimilarityOne():
    batchs = imageSimilarity.similarImagesDividedInLists(testImages,1)
    quantityOfBatchs = len(batchs)
    assert quantityOfBatchs == 21

def test_twentyOneBatchsFromTestImagesWithSimilarityOne():
    batchs = imageSimilarity.similarImagesDividedInLists(testImages,0)
    quantityOfBatchs = len(batchs)
    assert quantityOfBatchs == 1
