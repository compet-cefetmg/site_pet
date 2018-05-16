from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from members.models import Member
from site_pet.settings import MEDIA_ROOT
import os
import datetime


def get_image_path(instance, filename):
    if instance.id:
        thumbnail_path = os.path.join('blog', str(instance.id), 'thumb')
        if os.path.exists(os.path.join(MEDIA_ROOT, thumbnail_path)):
            os.remove(os.path.join(MEDIA_ROOT, thumbnail_path))
        return thumbnail_path
    return os.path.join('blog', filename)


class Post(models.Model):
    title = models.CharField('Título', max_length=255)
    member = models.ForeignKey(Member, on_delete=models.PROTECT, editable=False, null=True)
    text_call = models.CharField('Descrição', max_length=255)
    text_content = models.TextField('Conteúdo', )
    thumbnail = models.ImageField('Thumbnail', upload_to=get_image_path, null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True, auto_now_add=False)
    publish_as_team = models.BooleanField('Postar em nome da equipe', default=False)
    definitive = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.title
