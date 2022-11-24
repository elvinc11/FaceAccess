from django.db import models
from datetime import datetime
import os

# Create your models here.

class User(models.Model):
	id = models.CharField(primary_key=True, max_length=10)
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	def num_photos(self):
		try:
			DIR = f"app/facerec/dataset/{self.name}_{self.id}"
			img_count = len(os.listdir(DIR))
			return img_count
		except:
			return 0 


class Detected(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	time_stamp = models.DateTimeField()
	photo = models.ImageField(upload_to='detected/', default='app/facerec/detected/noimg.png')

	def __str__(self):
		user = User.objects.get(name=self.user_id)
		return f"{user.name} {self.time_stamp}"

class Website(models.Model):
	website_id = models.CharField(primary_key=True, max_length=10)
	url = models.CharField(max_length=500)
	
	def __str__(self):
		website = Website.objects.get(url=self.url)
		return {website.url}
