from django.db import models
from django.contrib.auth.models import User
from utils.upload_helper import get_image_path
import os
import datetime


class Campus(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Number')
    location = models.CharField(max_length=255)
    roman_id = models.CharField(max_length=2, editable=False)

    class Meta:
        verbose_name_plural = 'campi'

    def __str__(self):
        return 'Campus ' + self.roman_id + ' (' + self.location + ')'


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'curso'

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

    class Meta:
        verbose_name = 'PET'
        verbose_name_plural = 'Todos os PET'


class MyPet(Pet):

    class Meta:
        proxy = True
        verbose_name = 'Meu PET'
        verbose_name_plural = 'Meu PET'
