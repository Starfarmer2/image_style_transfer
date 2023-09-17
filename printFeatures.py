from model import YourModel
from PIL import Image
import torchvision.transforms as transforms
import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2


class ModelRunner:
    def __init__(self):
        self.device = torch.device("cpu")
        # self.device = torch.device("cuda")# if torch.cuda.is_available else "cpu")
        print(f'ModelRunner device: {self.device}')
        # self.device = torch.device("cpu")
        # Since we don't want to change the pretrained parameters in the model during our training process,
        # so we use .eval() means we are evaluating this model to "freeze" the parameters in the model.
        self.model = YourModel().to(self.device).eval()

        self.img_height = 224
        self.img_width = 224
        # Create a data loader to transform the image into tensors which our model can understand and work with.
        self.loader = self.set_loader()
        # Set the alpha and beta value
        self.alpha_value = 1
        self.beta_value = 2
        self.weights = [1, 1, 0.8, 0.1, 0.1]
        # Set a default original image and a default style image in case the user forgets to assign them.
        self.original_img = self.load_image("original.jpeg") * 256
        self.style_img = self.load_image("picasso2.jpeg") * 256

    def set_loader(self):
        return transforms.Compose([transforms.Resize((self.img_height, self.img_width)), transforms.ToTensor()])

    def load_image(self, image_name):
        image = Image.open(image_name)
        image = self.loader(image).unsqueeze(0)
        return image.to(self.device)

    def showFeatures(self, feature, name, height, width):
        im = feature.clone().detach()[0].numpy()
        im2 = np.array([[[im[c][i][j] / 256 for c in range(3)] for j in range(width)] for i in range(height)],
                       dtype='float64')
        cv2.imshow(name, im2)
        cv2.waitKey(0)


    def saveFeatures(self, feature, name, height, width):
        im = feature.clone().detach()[0].numpy()
        im2 = np.array([[[im[c][i][j] / 256 for c in range(3)] for j in range(width)] for i in range(height)],
                       dtype='float64')
        # print(f'SHAPE2: {im2.shape}')
        found = False
        coords = [0, 0, 0]
        for i in range(height):
            for j in range(width):
                for c in range(3):
                    if (im2[i][j][c] > 1):
                        found = True
                        coords = [i, j, c]
                        im2[i][j][c] = 1
                    elif (im2[i][j][c] < 0):
                        found = True
                        coords = [i, j, c]
                        im2[i][j][c] = 0
        plt.imsave(name, im2)

if __name__ == '__main__':
    runner = ModelRunner()
    features = runner.model.fd(runner.style_img)
    cnt = 0
    for feature in features:
        _, channel, height, width = feature.shape
        runner.showFeatures(feature, f'feature{cnt}', height, width)
        runner.saveFeatures(feature,f'feature{cnt}.png',height, width)
        cnt += 1
    cv2.destroyAllWindows()
