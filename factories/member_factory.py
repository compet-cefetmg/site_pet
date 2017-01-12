import factory
from factories.user_factory import UserFactory
from factories.cefet_factory import PetFactory
from members.models import Member, MemberRole
from faker import Faker


faker = Faker()


class MemberRoleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = MemberRole

    name = faker.name()
    name_plural = faker.name()


class MemberFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Member

    user = factory.SubFactory(UserFactory)
    name = faker.name()
    pet = factory.SubFactory(PetFactory)
    role = factory.SubFactory(MemberRoleFactory)
