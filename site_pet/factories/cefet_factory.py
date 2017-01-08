import factory
from cefet.models import *
from faker import Faker


faker = Faker()


class CampusFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Campus

    id = factory.Sequence(lambda n: n+1)
    location = faker.city()


class CourseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Course

    name = faker.name()
    campus = factory.SubFactory(CampusFactory)


class PetFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Pet

    course = factory.SubFactory(CourseFactory)
