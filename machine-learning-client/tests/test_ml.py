import emotion_recog as ml
import cv2
import pytest

class Test:
    def test_sanity_check(self):
        assert True == True, 'expect True to be True'

    '''
    Tests client's ability to correctly throw an error when no face is present in an image
    '''
    def test_image_with_no_face(self):
        img = cv2.imread('./test_images/clarinet.jpg')

        model = ml.Model()

        with pytest.raises(Exception):
            model.read_picture(img)
        # model.read_picture(img)

    def test_angry_face(self):
        img = cv2.imread('./test_images/angry.jpg')

        model = ml.Model()

        assert model.read_picture(img) == 'Angry'

    def test_disgust_face(self):
        img = cv2.imread('./test_images/disgust.jpg')

        model = ml.Model()

        assert model.read_picture(img) == 'Disgust'
    
    def test_sad_face(self):
        img = cv2.imread('./test_images/sad.jpg')

        model = ml.Model()

        assert model.read_picture(img) == 'Sad'

    def test_neutral_face(self):
        img = cv2.imread('./test_images/neutral.jpg')

        model = ml.Model()

        assert model.read_picture(img) == 'Neutral'
    
    def test_surprise_face(self):
        img = cv2.imread('./test_images/surprise.jpg')

        model = ml.Model()

        assert model.read_picture(img) == 'Surprise'

    def test_fear_face(self):
        img = cv2.imread('./test_images/fear.jpg')

        model = ml.Model()

        assert model.read_picture(img) == 'Fear'

    def test_happy_face(self):
        img = cv2.imread('./test_images/happy.jpg')

        model = ml.Model()

        assert model.read_picture(img) == 'Happy'
    
    def test_picture_capture(self):
        model = ml.Model()
        pic = model.cap_picture()
        assert len(pic) > 0