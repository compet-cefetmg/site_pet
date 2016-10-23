from django.contrib.auth.models import User, Group


def pets_processor(request):
    group = Group.objects.get(name='PET')
    users = group.user_set.all()
    return {'users': users}