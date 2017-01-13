import factory
from cefet.models import *


class CampusFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Campus

    id = factory.Sequence(lambda n: n+1)
    location = factory.Sequence(lambda n: 'City {0}'.format(n+1))


class CourseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Course

    name = factory.Sequence(lambda n: 'Course {0}'.format(n+1))
    campus = factory.SubFactory(CampusFactory)


class PetFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Pet

    course = factory.SubFactory(CourseFactory)
