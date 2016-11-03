from django.contrib.auth.models import User, Group


def pets_processor(request):
    try:
        group = Group.objects.get(name='PET')
        users = group.user_set.all()
    except Exception:
        users = User.objects.all()
    return {'users': users}
