import factory
from django.contrib.auth.models import User, Group


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user{0}'.format(n + 1))
    email = factory.Sequence(lambda n: 'user{0}@cefetmg.br'.format(n + 1))
    password = factory.PostGenerationMethodCall('set_password', 'password')


class GroupFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Group


class AdminGroupFactory(GroupFactory):

    name = 'admin'


class TutorsGroupFactory(GroupFactory):

    name = 'tutors'


class MembersGroupFactory(GroupFactory):

    name = 'members'
