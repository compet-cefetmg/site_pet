import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user{0}'.format(n + 1))
    email = factory.Sequence(lambda n: 'user{0}@cefetmg.br'.format(n + 1))
    password = factory.PostGenerationMethodCall('set_password', 'password')
