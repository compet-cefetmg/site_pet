from django.db import models
import os, datetime
from django.conf import settings
from members.models import Member

def get_image_path(instance, filename):
    # If publication is being created, saves image into temporary folder
    # Else, removes previous image and saves the new one
    if instance.id is not None:
        path = os.path.join(settings.MEDIA_ROOT, 'blog/thumbnails', str(instance.id))
        if os.path.isfile(path):
            os.remove(path)
        return os.path.join('blog/thumbnails', str(instance.id))
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
    member = models.ForeignKey(Member,verbose_name="Author",on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

class MyPublication(Publication):
    class Meta:
        proxy = True
