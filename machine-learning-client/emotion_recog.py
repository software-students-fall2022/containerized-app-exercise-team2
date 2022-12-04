import torch
import torch.nn as nn
import cv2 
from torchvision import datasets, models, transforms
from PIL import Image
import pymongo
import certifi
import sys
import datetime
from pathlib import Path

url = "mongodb+srv://admin:admin123@cluster0.b6toxnx.mongodb.net/?retryWrites=true&w=majority"
database=None
client=None
ca = certifi.where()

connection= pymongo.MongoClient(url, tlsCAFile=ca)
try:
    connection.admin.command('ping')
    client=connection
    database = connection["project_4"]
    print(' *', 'Connected to MongoDB!', file=sys.stderr)
except Exception as e:
    print(' *', "Failed to connect to MongoDB at", file=sys.stderr)
    print('Database connection error: ' + e, file=sys.stderr)

#Class for the machine learning model
class Model:
    #Creates the model and loads in the weights for the emotion recognition model I trained
    def __init__(self):
        # self.recog = str(Path('emotion_recog_1.pth').resolve())
        # self.cas = str(Path('haarcascade_frontalface_default.xml').resolve())
        # recog = str(Path('emotion_recog_1.pth').resolve())
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', weights = None)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 7)
        self.model.load_state_dict(torch.load("machine-learning-client/emotion_recog_1.pth", map_location=torch.device('cpu')))
        self.model.eval()
        self.emotions = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

    @staticmethod
    def cap_picture():
        capture = cv2.VideoCapture(0)
        __, pic = capture.read()
        # cv2.imread(pic)
        # cv2.imshow('capture', pic)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        capture.release()
        return pic

    @staticmethod
    def detect(pic):
        cas = 'haarcascade_frontalface_default.xml'
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cas)

        gray = cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)

        faces = cascade.detectMultiScale(gray, 1.1, 0)
        face = None
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
        
        return face

    @staticmethod
    def transform(face):
        pil_pic = Image.fromarray(face)

        data_transforms = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
        ])
        image = data_transforms(pil_pic)
        
        im_rep = image.repeat(3,1,1)
        normalize = transforms.Compose([
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        im_rep = normalize(im_rep)

        return im_rep.unsqueeze(0)

    #Takes a picture then transforms it for the model
    #The model then processes it and returns 
    def classify(self, pic = None):
        if pic is None:
            pic = self.cap_picture()
        
        face = self.detect(pic)

        if face is None:
            raise Exception('No faces detected') 
        
        im_rep = self.transform(face)
        outputs = self.model(im_rep)
        _, preds = torch.max(outputs, 1)
        return self.emotions[int(preds)]

def main():
    print('This app will make use of your camera to take a photo and analyze your mood.')
    print('Please head to URL_HERE to view a history of your moods.')
    model = Model()

    user = None
    while(True):
        username = input('Please enter your usename: ')
        user = database.user.find_one({'username': username})

        if user != None:
            break
        else:
            print('Username cannot be found!')

    # db.collection_name.find_one({'username': user, 'password': passwd})
    # model.cap_picture()
    print('Working...')
    mood = model.classify()
    database.mood.insert_one({
        'mood': mood,
        'time': datetime.datetime.now(),
        'user': user['_id']
    })
    print('Done!')

if __name__ == '__main__':
    main()
# temp = Model()
# pic = temp.read_picture()
# print(pic[0])