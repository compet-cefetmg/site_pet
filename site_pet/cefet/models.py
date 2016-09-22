from django.db import models
from django.contrib.auth.models import User
from utils.upload_helper import get_image_path
import os
import datetime


class Campus(models.Model):
    class Meta:
        verbose_name_plural = 'campi'

    id = models.IntegerField(primary_key=True, verbose_name='Number')
    location = models.CharField(max_length=255)
    roman_id = models.CharField(max_length=2, editable=False)

    def __str__(self):
        return 'Campus ' + self.roman_id + ' (' + self.location + ')'


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)

    def __str__(self):
        return self.name +  ' (Campus ' + self.campus.roman_id + ')'


class Pet(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to=get_image_path)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    start = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.course.__str__()


class MyPet(Pet):
    class Meta:
        proxy = True
