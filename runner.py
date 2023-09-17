import torch
import torch.optim as optim
from torch.autograd import Variable
from PIL import Image
import torchvision.transforms as transforms
from torchvision.utils import save_image
from model import YourModel
import matplotlib.pyplot as plt
import numpy as np

# This is the class which does the actual image generation job for you.
# This class use the model you defined in the model.py file and trains the model.

class ModelRunner:
	def __init__(self,STYLE_IMAGE,ORIGINAL_IMAGE):
		self.device = torch.device("cpu")
		#self.device = torch.device("cuda")
		print(f'ModelRunner device: {self.device}')
		self.model = YourModel().to(self.device).eval()
		self.img_height = 224
		self.img_width = 224
		self.loader = self.set_loader()
		self.alpha_value = 1
		self.beta_value = 10
		self.weights = [1,1,0.8,0.3,0.3]
		self.original_img = self.load_image(ORIGINAL_IMAGE)
		self.style_img = self.load_image(STYLE_IMAGE)
		# self.generated_img = Variable(torch.randn(self.original_img.shape), requires_grad=True) #cuda
		self.generated_img = self.original_img.clone()
		self.generated_img.requires_grad_(True)
		self.learning_rate = 5.0
		self.optimizer = optim.Adam([self.generated_img], lr=self.learning_rate)
		self.latest_gen_name = "00o.jpg"
		self.output_interval = 10
		self.scheduler = torch.optim.lr_scheduler.StepLR(self.optimizer, step_size=40, gamma=0.5)
		print("Image Height: % 4d, Image Width: % 4d" % (self.img_height, self.img_width))
		print("Optimizer:")
		print(self.optimizer)

	def set_loader(self):
		return transforms.Compose([transforms.Resize((self.img_height, self.img_width)), transforms.ToTensor()])
	
	def load_image(self, image_name):
		image = Image.open(image_name)
		image = self.loader(image).unsqueeze(0)
		return image.to(self.device)*256

	def set_original_image(self,address):
		self.original_img = self.load_image(address)

	def set_style_image(self,address):
		self.style_img = self.load_image(address)
	
	def set_alpha_beta(self, alpha, beta):
		if alpha > 0 and beta > 0:
			self.alpha_value = alpha
			self.beta_value = beta
		else:
			self.alpha_value = 1
			self.beta_value = 0.4
			
	def set_image_size(self, height, width):
		self.img_height = height
		self.img_width = width

	def set_output_interval(self, interval):
		if interval > 0:
			self.output_interval = interval
			
	def get_output_interval(self):
		return self.output_interval
	
	#calculate style and original features, static throughout process
	def calculate_os_features(self):
		# self.style_features = self.model.fd(self.style_img.cuda())
		# self.original_features = self.model.fd(self.original_img.cuda())
		self.style_features = self.model.fd_style(self.style_img)
		self.original_features = self.model.fd_content(self.original_img)

	def train_one_step(self, step):
		self.generated_content_features = self.model.fd_content(self.generated_img)
		self.generated_style_features = self.model.fd_style(self.generated_img)

		feature_group = zip(self.generated_content_features, self.generated_style_features, self.original_features, self.style_features)

		style_loss = torch.FloatTensor(1).zero_().requires_grad_(True)
		content_loss = torch.FloatTensor(1).zero_().requires_grad_(True)
		layer = 0
		for g_content_feature, g_style_feature, o_feature, s_feature in feature_group:
			content_batch_size, content_channel, content_height, content_width = g_content_feature.shape
			style_batch_size, style_channel, style_height, style_width = g_style_feature.shape
			content_loss = content_loss + torch.mean((g_content_feature-o_feature)**2).div(content_channel*content_height*content_width)

			Gram_gen = g_style_feature.view(style_channel,style_height*style_width).mm(g_style_feature.view(style_channel,style_height*style_width).t()).div(style_channel*style_height*style_width)
			Gram_sty = s_feature.view(style_channel,style_height*style_width).mm(s_feature.view(style_channel,style_height*style_width).t()).div(style_channel*style_height*style_width)
			style_loss = style_loss + self.weights[layer] * torch.mean((Gram_gen-Gram_sty)**2)
			layer += 1
		total_loss = self.alpha_value * content_loss + self.beta_value * style_loss
		self.optimizer.zero_grad()

		total_loss.backward(retain_graph=True)

		self.optimizer.step()
		self.scheduler.step(epoch=step)

		if step % self.output_interval == 0:

			print(f'loss: {total_loss}')
			# Store the file name
			self.latest_gen_name = "generated" + str(step) + ".png"

			im = self.generated_img.clone().detach()[0].numpy()
			im = np.swapaxes(im,0,1)
			im = np.swapaxes(im,1,2)/256
			clipped_im = np.clip(im,0,1)

			plt.imsave('ResultImages/'+self.latest_gen_name,clipped_im)
