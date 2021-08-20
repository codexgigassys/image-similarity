import sys
import cv2
import os
from imageSimilarity import Image
import testing_configuration

sys.path.append('../')
sys.path.append('tests')


def test_imageReturnsName06jpeg():
    anImage = Image('tests/testImages/06.jpeg')
    return anImage.name == "06.jpeg"


def test_imageReturnsName01jpeg():
    anImage = Image('tests/testImages/01.jpeg')
    return anImage.name == "01.jpeg"
