import sys
import cv2
import os
from imageSimilarity import Image
sys.path.append('../')
sys.path.append('tests')
import testing_configuration

def test_imageReturnsName06jpeg():
    anImage = Image('tests/testImages/06.jpeg')
    return anImage.name == "06.jpeg"


def test_imageReturnsName01jpeg():
    anImage = Image('tests/testImages/01.jpeg')
    return anImage.name == "01.jpeg"
