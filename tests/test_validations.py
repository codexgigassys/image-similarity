import sys
import cv2
import imageSimilarity
from imageSimilarity import Image

sys.path.append('../')
testImages = Image.allFromPath('/image-similarity/tests/testImages/')


def test_twoEqualImagesHasSimilarityOne():

    imageOne = Image.fromPath('tests/testImages/01.jpeg')
    imageTwo = Image.fromPath('tests/testImages/01.jpeg')

    result = imageOne.similarityWith(imageTwo)

    assert result == 1


def test_twoNotSimilarImagesHasLowSimilarity():
    imageOne = Image.fromPath('tests/testImages/01.jpeg')
    imageTwo = Image.fromPath('tests/testImages/03.jpeg')

    result = imageOne.similarityWith(imageTwo)

    assert result < 0.25


def test_twoSimilarImagesHasHighSimilarity():
    imageOne = Image.fromPath('tests/testImages/01.jpeg')
    imageTwo = Image.fromPath('tests/testImages/02.jpeg')

    result = imageOne.similarityWith(imageTwo)

    assert result > 0.9


def test_fiveBatchsFromTestImagesWithHighSimilarity():
    batchs = imageSimilarity.similarImagesDividedInLists(testImages, 0.95)
    quantityOfBatchs = len(batchs)
    assert quantityOfBatchs == 5


def test_twentyOneBatchsFromTestImagesWithSimilarityOne():
    batchs = imageSimilarity.similarImagesDividedInLists(testImages, 1)
    quantityOfBatchs = len(batchs)
    assert quantityOfBatchs == 21


def test_twentyOneBatchsFromTestImagesWithSimilarityOne():
    batchs = imageSimilarity.similarImagesDividedInLists(testImages, 0)
    quantityOfBatchs = len(batchs)
    assert quantityOfBatchs == 1
