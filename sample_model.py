import torch
import torch.nn as nn
# import some activation function
import torch.nn.functional as F

# You need to build your own neural network based on pretrained models provided by PyTorch
# A custom PyTorch neural network has two essential functions: the __init__() function and the forward() function.

some_number = 10


class SampleConvNet(nn.Module):
	def __init__(self):
		super(SampleConvNet, self).__init__()
		self.variable0 = some_number
		self.some_empty_list = []
		self.convolution_layer_1 = nn.Conv2d(in_channels=3, out_channels=10, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
		self.convolution_layer_2 = nn.Conv2d(in_channels=10, out_channels=15, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
		self.pooling_layer = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
		self.fully_connected_layer_1 = nn.Linear(in_features=16*7*7, out_features=some_number)
		
	def forward(self, x):
		x = F.relu(self.convolution_layer_1(x))
		x = self.pooling_layer(x)
		x = F.relu(self.convolution_layer_2(x))
		x = x.reshape(x.shape[0], -1)
		x = self.fully_connected_layer_1(x)
		return x


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x = torch.randn((3, 224, 224), device=device)
model = SampleConvNet().to(device).eval()
output = model(x)