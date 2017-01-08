from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from django.utils.six import BytesIO
from PIL import Image
from members.models import Member, MemberRole
from factories.member_factory import MemberFactory


faker = Faker()


class PostTestCase(TestCase):

    def setUp(self):
        Group.objects.create(name='members')
        Group.objects.create(name='tutors')
        self.member = MemberFactory()
        self.member.user.groups.add(Group.objects.get(name='members'))

    def test_post_should_return_unauthorized(self):
        response = self.client.get(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 302)

    def test_post_form_should_be_loaded(self):
        self.client.login(username=self.member.user.username,
                          password='password')
        self.assertTrue(self.member.user.is_authenticated())
        response = self.client.get(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 200)

    def test_post_should_not_be_created(self):
        self.client.login(username=self.member.user.username,
                          password='password')
        self.assertTrue(self.member.user.is_authenticated())
        response = self.client.post(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 400)

    def test_post_should_be_created(self):
        self.client.login(username=self.member.user.username,
                          password='password')
        self.assertTrue(self.member.user.is_authenticated())
        thumbnail = SimpleUploadedFile(name='thumb.png', content=open(
            'mediafiles/thumb.png', 'rb').read(), content_type='image/png')
        post = {
            'text_call': faker.sentence(),
            'title': faker.sentence(),
            'author': faker.name(),
            'text_content': faker.text(),
            'thumbnail': thumbnail,
        }
        response = self.client.post(reverse('blog.add_post'), post)
        self.assertEqual(response.status_code, 302)
