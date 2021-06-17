import sys
import cv2
import os
sys.path.append('../')
from imageSimilarity import Image
sys.path.append('tests')

def test_imageReturnsName06jpeg():
    anImage = Image('testImages/06.jpeg')
    return anImage.name == "06.jpeg"

def test_imageReturnsName01jpeg():
    anImage = Image('testImages/01.jpeg')
    return anImage.name == "01.jpeg"