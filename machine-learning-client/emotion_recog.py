import torch
import torch.nn as nn
import cv2 
from PIL import Image

class model:
    def __init__(self):
        model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', weights = None)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, 7)
        model.load_state_dict(torch.load("emotion_recog_1.pth"))
        model.eval()

    def read_picture(self, pic = None):
        #Convert to tensor and standardize pic
        if not pic:
            pic = self.take_picture()
        cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
        return model(pic)
    
    def take_picture():
        return VideoCapture(0).read()

