from django.contrib.auth.models import User


def pets_processor(request):
    return {'users': User.objects.all()}