import sys
import os
sys.path.append('../')
import imageSimilarity
sys.path.append('tests')

def test_batchOfFilesIsSavedInSpecifiedPath():
    images = imageSimilarity.imagesInPath("testImages")
    batchs = imageSimilarity.similarImagesDividedInBatchs(images,0.95)
    imageSimilarity.saveBatchOfImages(batchs,'testResult')
    assert len(os.listdir('testResult')) == 5