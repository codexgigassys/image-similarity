import sys
#The following line is done to get the imageSimilarity.py that is in the previous folder.
sys.path.append('../')
import imageSimilarity

def test_aSimilarityGradeBelowZeroIsNotValid():
    assert not imageSimilarity.isValidSimilarityGrade(-0.4)

def test_aSimilarityGradeEqualToZeroIsValid():
    assert imageSimilarity.isValidSimilarityGrade(0)

def test_aSimilarityGradeEqualToOneIsValid():
    assert imageSimilarity.isValidSimilarityGrade(1)

def test_aSimilarityGradeGreaterThanZeroAndBelowOneIsValid():
    assert imageSimilarity.isValidSimilarityGrade(0.5)

def test_aSimilarityGradeGreaterThanOneIsNotValid():
    assert not imageSimilarity.isValidSimilarityGrade(1.6)

def test_aStringIsNotAValidDirectoryPath():
    assert not imageSimilarity.isValidDirectoryPath("xxxXXXxxx-*/-.,")

def test_aStringisAValidDirectoryPath():
    assert imageSimilarity.isValidDirectoryPath(".")