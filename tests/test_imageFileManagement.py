import sys
import cv2
import os
sys.path.append('../')
import imageSimilarity
sys.path.append('tests')

def test_batchOfFilesIsSavedInSpecifiedPath():
    images = imageSimilarity.imagesInPath("testImages")
    batchs = imageSimilarity.similarImagesDividedInLists(images,0.95)
    imageSimilarity.saveImagesInLists(batchs,'testResult')
    assert len(os.listdir('testResult')) == 5


def test_imageHashReturnExpectedValue():
    anImageFile = open('testImages/06.jpeg','rb')
    return imageSimilarity.hashBuffer(anImageFile.read()) == "4dedb7caab44c5b65ba0692cc54a5f2735dee5f4"