import factory
from factories.auth_factory import UserFactory
from factories.cefet_factory import PetFactory
from members.models import Member, MemberRole


class MemberRoleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = MemberRole

    name = factory.Sequence(lambda n: 'Role {0}'.format(n + 1))
    verbose_name = factory.Sequence(lambda n: 'Verbose {0} plural'.format(n + 1))
    verbose_name_plural = factory.Sequence(lambda n: 'Verbose {0} plural'.format(n + 1))


class MemberFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Member

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: 'Member {0}'.format(n + 1))
    pet = factory.SubFactory(PetFactory)
    role = factory.SubFactory(MemberRoleFactory)
