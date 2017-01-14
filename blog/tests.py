from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from factories.member_factory import *
from factories.auth_factory import *
from factories.blog_factory import PostFactory


faker = Faker()


class PostTestCase(TestCase):

    def setUp(self):
        self.roles = {}
        for role in ['admin', 'tutor', 'scholar', 'volunteer', 'contributor', 'ex-member']:
            self.roles[role] = MemberRoleFactory(name=role)
        self.member = MemberFactory(role=self.roles['scholar'])
        self.posts = PostFactory.create_batch(5)

    def test_index_page_should_return_200(self):
        response = self.client.get(reverse('blog.index'))
        self.assertEqual(response.status_code, 200)

    def test_5_posts_should_be_loaded(self):
        self.assertEqual(len(self.posts), 5)
        for post in self.posts:
            response = self.client.get(reverse('blog.post', kwargs={'id': post.id}))
            self.assertEqual(response.status_code, 200)

    def test_should_return_no_post_found(self):
        response = self.client.get(reverse('blog.post', kwargs={'id': 0}))
        self.assertEqual(response.status_code, 404)

    def test_post_should_return_unauthorized(self):
        response = self.client.get(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 302)

    def test_post_form_should_be_loaded(self):
        self.client.login(username=self.member.user.username, password='password')
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
        self.client.login(username=self.member.user.username, password='password')
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

    def test_post_should_be_deleted_by_author(self):
        self.client.login(username=self.member.user.username, password='password')
        post = PostFactory(member=self.member)
        response = self.client.post(reverse('blog.delete_post'), {'id': post.id})
        self.assertEqual(response.status_code, 200)

    def test_post_should_be_deleted_by_pet_member(self):
        pet_member = MemberFactory(pet=self.member.pet)
        self.client.login(username=pet_member.user.username, password='password')
        post = PostFactory(member=self.member)
        response = self.client.post(reverse('blog.delete_post'), {'id': post.id})
        self.assertEqual(response.status_code, 200)

    def test_post_should_not_be_deleted_by_non_pet_member(self):
        post = PostFactory(member=self.member)
        other_member = MemberFactory()
        self.client.login(username=other_member.user.username, password='password')
        response = self.client.post(reverse('blog.delete_post'), {'id': post.id})
        self.assertEqual(response.status_code, 403)

    def test_json_should_have_data_attr_with_array_of_4_elements(self):
        self.client.login(username=self.member.user.username, password='password')
        PostFactory.create_batch(5, member=self.member)
        response = self.client.get(reverse('blog.all'))
        self.assertTrue('data' in response.json())
        self.assertEqual(5, len(response.json()['data']))
        for item in response.json()['data']:
            self.assertEqual(4, len(item))
