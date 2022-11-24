import torch
from PIL import Image

class model:
    def __init__(self):
        model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', weights = None)
        model.load_state_dict(torch.load("emotion_recog_1.pth"))
        model.eval()

    def read_picture(self, pic):
        #Convert to black and white then tesnor and standardize pic
        return model(pic)
