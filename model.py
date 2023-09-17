import torch.nn as nn
import torch
import numpy as np
import torchvision.models as models

class YourModel(nn.Module):
	def __init__(self):
		super(YourModel, self).__init__()
		# self.device = torch.device("cuda" if torch.cuda.is_available else "cpu")
		self.device = torch.device("cpu")
		self.model_features = models.vgg19().to(self.device).features
		for i in range(len(self.model_features)):
			if isinstance(self.model_features[i],nn.ReLU):
				self.model_features[i] = nn.ReLU(inplace=False)
		print(f'YourModel device: {self.device}')
		self.chosen_content_feature_layers = [22,31]
		self.chosen_style_feature_layers = [0,5,10,19,28]#[3,8,17,26,35]#[0,5,10,19,28]  #'0', '5', '10', ...
		#self.chosen_feature_layers = [1]

	def fd(self, x):
		features = []
		index = 0
		for i in range(len(self.model_features)):
			x = self.model_features[i](x).requires_grad_(True)
			features.append(x)
		return features

	def fd_content(self, x):
		features = []

		index = 0
		for i in range(len(self.model_features)):
			x = self.model_features[i](x).requires_grad_(True)
			if index < len(self.chosen_content_feature_layers) and i == self.chosen_content_feature_layers[index]:
				index += 1
				features.append(x)
		return features


	def fd_style(self, x):
		features = []
		
		index = 0
		for i in range(len(self.model_features)):
			x = self.model_features[i](x).requires_grad_(True)
			if index < len(self.chosen_style_feature_layers) and i == self.chosen_style_feature_layers[index]:
				index += 1
				features.append(x)
		return features