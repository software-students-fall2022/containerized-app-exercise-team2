import pytest
import sys
import cv2
from pathlib import Path
import emotion_recog as ml

class Test:
    def test_sanity_check(self):
        assert True == True, 'expect True to be True'

    '''
    Tests function's ability to return None when no face is present in an image
    '''
    def test_image_with_no_face(self):
        #rel_path = Path.cwd() / 'test_images' / 'clarinet.jpg'
        #abs_path = str(rel_path.resolve())
        #abs_path = str(Path('clarinet.jpg').resolve())
        #abs_path = 'C:/Users/John Kolibachuk/Desktop/NYU/Fall 2022/software_engineering/containerized-app-exercise-team2-1/machine-learning-client/tests/clarinet.jpg'
        path = "machine-learning-client/tests/clarinet.jpg"
        img = cv2.imread(path)
        #img = cv2.imread('/clarinet.jpg')

        face = ml.Model.detect(img)

        assert face == None, 'expected value of face to be None'

    '''
    Tests function's ability to correctly identify a face
    '''
    def test_face_recognition(self):
        img_path = str(Path('machine-learning-client/tests/neutral.jpg').resolve())
        img = cv2.imread(img_path)

        face = ml.Model.detect(img)

        assert face != None, 'expected value of face to not be None'

    '''
    Ensures camera is working and an image is successfully captured
    '''
    def test_picture_capture(self):
        pic = ml.Model.cap_picture()
        assert len(pic) > 0, 'expected image array with len > 0 to be returned'

    '''
    Ensures that picture is correctly transformed to tensor
    '''
    def test_transform(self):
        img_path = str(Path('machine-learning-client/tests/neutral.jpg').resolve())
        img = cv2.imread(img_path)
        face = ml.Model.detect(img)
        trans = ml.Model.transform(face)

        assert len(trans) == 1, 'expected length 1 array'

    def test_angry_face(self):
        img = cv2.imread('machine-learning-client/tests/angry.jpg')

        model = ml.Model()

        assert model.classify(img) == 'Angry'

    def test_disgust_face(self):
        img = cv2.imread('machine-learning-client/tests/disgust.jpg')

        model = ml.Model()

        assert model.classify(img) == 'Disgust'
    
    def test_sad_face(self):
        img = cv2.imread('machine-learning-client/tests/sad.jpg')

        model = ml.Model()

        assert model.classify(img) == 'Sad'

    def test_neutral_face(self):
        img = cv2.imread('machine-learning-client/tests/neutral.jpg')

        model = ml.Model()

        assert model.classify(img) == 'Neutral'
    
    def test_surprise_face(self):
        img = cv2.imread('machine-learning-client/tests/surprise.jpg')

        model = ml.Model()

        assert model.classify(img) == 'Surprise'

    def test_fear_face(self):
        img = cv2.imread('machine-learning-client/tests/fear.jpg')

        model = ml.Model()

        assert model.classify(img) == 'Fear'

    def test_happy_face(self):
        img = cv2.imread('machine-learning-client/tests/happy.jpg')

        model = ml.Model()

        assert model.classify(img) == 'Happy'

