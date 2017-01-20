import factory
from factories.auth_factory import UserFactory
from factories.cefet_factory import PetFactory
from members.models import Member, MemberRole
from django.core.files.uploadedfile import SimpleUploadedFile


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
    photo = SimpleUploadedFile(name='thumb.png', content=open(
        'mediafiles/thumb.png', 'rb').read(), content_type='image/png')
    facebook_link = 'https://facebook.com'
    lattes_link = 'https://lattes.cnpq.br'
