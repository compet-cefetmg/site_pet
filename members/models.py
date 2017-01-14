from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os
import datetime
from cefet.models import Pet


class MemberRole(models.Model):
    name = models.CharField(max_length=255, unique=True)
    verbose_name = models.CharField(max_length=255, unique=True)
    verbose_name_plural = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Função do membro'
        verbose_name_plural = 'Funções dos membros'

    def __str__(self):
        return self.verbose_name.capitalize()


def get_image_path(instance, filename):
    return 'members/' + filename.split('/')[-1]


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Nome', max_length=255)
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT, related_name='members', null=True, blank=True)
    photo = models.ImageField('Foto', max_length=255, upload_to=get_image_path, blank=True)
    facebook_link = models.CharField('Link do Facebook', max_length=255, blank=True)
    lattes_link = models.CharField('Link do Lattes', max_length=255, blank=True)
    role = models.ForeignKey(MemberRole, on_delete=models.PROTECT, related_name='members', verbose_name='Função')

    def __str__(self):
        return self.name
