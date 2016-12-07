from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os
import datetime
from cefet.models import Pet


class MemberRole(models.Model):
    name = models.CharField('Nome', max_length=255, unique=True)
    name_plural = models.CharField('Plural', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Papel do membro'
        verbose_name_plural = 'Papéis dos membros'

    def __str__(self):
        return self.name


def get_image_path(instance, filename):
    return 'members/' + filename.split('/')[-1]


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT, related_name='members')
    name = models.CharField('Nome', max_length=255)
    photo = models.ImageField('Foto', max_length=255, upload_to=get_image_path, blank=True)
    facebook_link = models.CharField('Link do Facebook', max_length=255, blank=True)
    lattes_link = models.CharField('Link do Lattes', max_length=255, blank=True)
    email = models.EmailField('E-mail', max_length=255, blank=True)
    role = models.ForeignKey(MemberRole, on_delete=models.PROTECT, related_name='members', verbose_name='Papel')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Membros (todos)'


class MyMember(Member):
    class Meta:
        proxy = True
        verbose_name = 'Membro'
