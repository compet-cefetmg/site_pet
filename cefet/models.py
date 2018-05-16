from django.db import models
from django.contrib.auth.models import User
import os
import datetime


class Campus(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Número')
    location = models.CharField('Cidade', max_length=255)
    roman_id = models.CharField(max_length=10, editable=False)

    class Meta:
        verbose_name_plural = 'campi'

    def __str__(self):
        return 'Campus ' + self.roman_id + ' (' + self.location + ')'


class Course(models.Model):
    name = models.CharField('Nome', max_length=255, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'curso'

    def __str__(self):
        return self.name +  ' (Campus ' + self.campus.roman_id + ')'


def get_image_path(instance, filename):
    return 'cefet/' + filename.split('/')[-1]


class Pet(models.Model):
    photo = models.ImageField('Foto', upload_to=get_image_path, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='Curso')
    start = models.DateField('Data de criação', blank=True, null=True)
    description = models.TextField('Descrição', blank=True, null=True)

    def __str__(self):
        return self.course.__str__()
