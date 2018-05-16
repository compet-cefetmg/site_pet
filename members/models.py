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
        verbose_name = 'função do membro'
        verbose_name_plural = 'funções dos membros'

    def __str__(self):
        return self.verbose_name.capitalize()


def get_image_path(instance, filename):
    return 'members/' + filename.split('/')[-1]


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField('E-mail', max_length=255, null=True, unique=True)
    name = models.CharField('Nome', max_length=255)
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT, related_name='members', null=True)
    photo = models.ImageField('Foto', max_length=255, upload_to=get_image_path, blank=True)
    facebook_link = models.CharField('Link do Facebook', max_length=255, blank=True)
    lattes_link = models.CharField('Link do Lattes', max_length=255, blank=True)
    github_link = models.CharField('Link do GitHub', max_length=255, blank=True)
    mensage_ex_petiano = models.CharField('Mensagem ex-petiano', max_length=300, blank=True, null=True)
    start_date = models.DateField('Data de entrada no PET', null=True)
    leave_date = models.DateField('Data de saída do PET', null=True, blank=True)
    role = models.ForeignKey(MemberRole, on_delete=models.PROTECT, related_name='members', verbose_name='Função')
    autorized = models.BooleanField('Autorizado', default=False)
    d3v3l0p3r = models.BooleanField('Desenvolvedor', default=False)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'membro'
