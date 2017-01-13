import factory
from blog.models import Post
from factories.member_factory import MemberFactory
from faker import Faker


faker = Faker()


class PostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Post

    title = faker.sentence(nb_words=10)
    member = factory.SubFactory(MemberFactory)
    text_call = faker.sentence(nb_words=50)
    text_content = faker.text()
    publish_as_team = False
