from django.db import models
from django.contrib.auth.models import User
from utils.upload_helper import get_image_path
import os
import datetime


class Pet(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	photo = models.ImageField(upload_to=get_image_path)
	campus = models.IntegerField()
	course = models.CharField(max_length=255)
	start = models.DateField()
	description = models.TextField()

	def __str__(self):
		return self.course + ' (Campus ' + str(self.campus) + ')'
