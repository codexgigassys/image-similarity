import sys
import os
sys.path.append('../')
import imageSimilarity
from imageSimilarity import Image
sys.path.append('tests')

def test_batchOfFilesIsSavedInSpecifiedPath():
    images = Image.allFromPath("testImages")
    batchs = imageSimilarity.similarImagesDividedInLists(images,0.95)
    imageSimilarity.saveImagesInLists(batchs,'testResult')
    assert len(os.listdir('testResult')) == 5

def test_imageSHA1HashReturnExpectedValueFromBuffer():
    anImageFile = Image.fromBuffer(open('testImages/06.jpeg','rb').read())
    return anImageFile.sha1() == "4dedb7caab44c5b65ba0692cc54a5f2735dee5f4"

def test_imageSHA1HashReturnExpectedValueFromPathFile():
    anImageFile = Image.fromPath('testImages/06.jpeg')
    return anImageFile.sha1() == "4dedb7caab44c5b65ba0692cc54a5f2735dee5f4"