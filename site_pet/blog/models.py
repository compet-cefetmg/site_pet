from django.db import models
import os, datetime
from django.views.generic import TemplateView

def get_image_path(instance, filename):
    return os.path.join('blog/thumbnails', datetime.datetime.now().strftime('%Y%m%d%H%M%S'), filename)

class Publication(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    user = models.CharField(max_length=255, editable=False)
    text_call = models.CharField(max_length=255)
    text_content = models.TextField()
    thumbnail = models.ImageField(upload_to=get_image_path)
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    last_modification = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

class MyPublication(Publication):
    class Meta:
        proxy = True
