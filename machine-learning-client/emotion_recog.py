import torch
import torch.nn as nn
import cv2 
from torchvision import datasets, models, transforms
from PIL import Image

#Class for the machine learning model
class Model:
    #Creates the model and loads in the weights for the emotion recognition model I trained

    def __init__(self):
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', weights = None)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 7)
        self.model.load_state_dict(torch.load("machine-learning-client/emotion_recog_1.pth", map_location=torch.device('cpu')))
        self.model.eval()
        self.emotions = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

    #Takes a picture then transforms it for the model
    #The model then processes it and returns 
    def read_picture(self, pic = None):
        if not pic:
            capture = cv2.VideoCapture(0)
            __, pic = capture.read()
        cascade = cv2.CascadeClassifier('machine-learning-client/haarcascade_frontalface_default.xml')
        # cv2.imshow('window',pic)
        # cv2.waitKey(0) 
        # cv2.destroyAllWindows() 
        gray = cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.1, 0)
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
        if not face:
            raise Exception('No faces detected') 
        capture.release()
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
        outputs = self.model(im_rep.unsqueeze(0))
        _, preds = torch.max(outputs, 1)
        return self.emotions[int(preds)]

# temp = Model()
# pic = temp.read_picture()
# print(pic[0])
