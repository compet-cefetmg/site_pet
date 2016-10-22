from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from utils.upload_helper import get_image_path
import os
import datetime


class MemberRole(models.Model):
    name = models.CharField(max_length=255, unique=True)
    name_plural = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Papel do membro'
        verbose_name_plural = 'Papéis dos membros'

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(max_length=255, upload_to=get_image_path, blank=True)
    facebook_link = models.CharField(max_length=255, blank=True)
    lattes_link = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    email = models.EmailField(max_length=255, blank=True)
    role = models.ForeignKey(MemberRole, on_delete=models.PROTECT, related_name='members')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Todos os membros'


class MyMember(Member):
    class Meta:
        proxy = True
        verbose_name = 'Membro do meu PET'
        verbose_name_plural = 'Membros do meu PET'
