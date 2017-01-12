import factory
from django.contrib.auth.models import User
from faker import Faker


faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = faker.simple_profile()['username']
    email = faker.simple_profile()['mail']
    password = factory.PostGenerationMethodCall('set_password', 'password')
