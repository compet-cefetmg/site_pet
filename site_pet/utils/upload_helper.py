import os
import datetime
from django.conf import settings


def get_image_path(instance, filename):
    save_path = os.path.join(instance.__class__.__name__, 'images')
    if instance.id is not None:
        path = os.path.join(settings.MEDIA_ROOT, save_path, str(instance.id))
        if os.path.isfile(path):
            os.remove(path)
        return os.path.join(save_path, str(instance.id))
    return os.path.join(save_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S'), filename)
