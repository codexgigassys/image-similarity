import sys
import os
import imageSimilarity
from imageSimilarity import Image
sys.path.append('../')
sys.path.append('tests')
import testing_configuration


def test_batchOfFilesIsSavedInSpecifiedPath():
    images = Image.allFromPath("tests/testImages")
    batchs = imageSimilarity.similarImagesDividedInLists(images, 0.95)
    imageSimilarity.saveImagesInLists(batchs, 'tests/testResult')
    assert len(os.listdir('tests/testResult')) == 5


def test_imageSHA1HashReturnExpectedValueFromBuffer():
    anImageFile = Image.fromBuffer(open('tests/testImages/06.jpeg', 'rb').read())
    assert anImageFile.sha1() == "dd3e4d1e0a5730c9ea87175cf5a6516c27167836"


def test_imageSHA1HashReturnExpectedValueFromPathFile():
    anImageFile = Image.fromPath('tests/testImages/01.jpeg')
    assert anImageFile.sha1() == "52d57c19cc025fe44827e0970fa35d8ba5a5441f"


def test_anotherImageSHA1HashReturnExpectedValueFromBuffer():
    anImageFile = Image.fromBuffer(open('tests/testImages/10.jpeg', 'rb').read())
    assert anImageFile.sha1() == "1aeaca021d2934d0c4ffaccc6d44a0de3a3088ba"


def test_anotherImageSHA1HashReturnExpectedValueFromPathFile():
    anImageFile = Image.fromPath('tests/testImages/15.jpeg')
    assert anImageFile.sha1() == "f90bbb80a882ed63c650842a63732227cdd77937"
