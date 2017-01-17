from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from factories.member_factory import *
from factories.auth_factory import *
from factories.blog_factory import PostFactory
from blog.models import Post


faker = Faker()


def generate_post_form_data():
    thumbnail = SimpleUploadedFile(name='thumb.png', content=open(
        'mediafiles/thumb.png', 'rb').read(), content_type='image/png')
    return {'text_call': faker.sentence(), 'title': faker.sentence(), 'text_content': faker.text(), 'thumbnail': thumbnail}


class PostTestCase(TestCase):

    def setUp(self):
        self.roles = {}
        for role in ['admin', 'tutor', 'scholar', 'volunteer', 'contributor', 'ex-member']:
            self.roles[role] = MemberRoleFactory(name=role)

        self.member = MemberFactory(role=self.roles['scholar'])

    def test_index_page_should_return_200(self):
        response = self.client.get(reverse('blog.index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_should_return_404(self):
        response = self.client.get(reverse('blog.index'), {'pet': 0})
        self.assertEqual(response.status_code, 404)

    def test_index_page_should_return_given_pet_posts_only(self):
        posts = PostFactory.create_batch(5, member=self.member)
        PostFactory.create_batch(5)

        response = self.client.get(reverse('blog.index'), {'pet': self.member.pet.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(5, len(response.context['posts']))

        for post in response.context['posts']:
            self.assertIn(post, posts)

    def test_post_page_should_be_loaded(self):
        post = PostFactory()

        response = self.client.get(reverse('blog.post', kwargs={'id': post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], post)

    def test_post_page_should_return_404(self):
        response = self.client.get(reverse('blog.post', kwargs={'id': 0}))
        self.assertEqual(response.status_code, 404)

    def test_add_form_should_not_be_loaded(self):
        response = self.client.get(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 302)

    def test_add_form_should_be_loaded(self):
        self.client.login(username=self.member.user.username, password='password')
        response = self.client.get(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 200)

    def test_add_form_should_return_400(self):
        self.client.login(username=self.member.user.username, password='password')
        data = generate_post_form_data()
        data.pop('thumbnail', None)

        for key in data:
            value = data.pop(key)
            response = self.client.post(reverse('blog.add_post'), data)
            self.assertEqual(response.status_code, 400)
            data[key] = value

    def test_post_should_be_created(self):
        self.client.login(username=self.member.user.username, password='password')
        response = self.client.post(reverse('blog.add_post'), generate_post_form_data())
        self.assertEqual(response.status_code, 302)

    def test_edit_form_should_return_not_be_loaded(self):
        post = PostFactory(member=self.member)
        self.client.login(username=MemberFactory().user.username, password='password')
        response = self.client.get(reverse('blog.edit_post', kwargs={'id': post.id}))
        self.assertEqual(response.status_code, 403)

    def test_edit_form_should_be_loaded(self):
        post = PostFactory(member=self.member)
        self.client.login(username=self.member.user.username, password='password')
        response = self.client.get(reverse('blog.edit_post', kwargs={'id': post.id}))
        self.assertEqual(response.status_code, 200)

    def test_edit_form_should_be_invalid(self):
        post = PostFactory(member=self.member)
        self.client.login(username=self.member.user.username, password='password')
        response = self.client.post(reverse('blog.edit_post', kwargs={'id': post.id}))
        self.assertEqual(response.status_code, 400)

    def test_post_should_be_edited(self):
        post = PostFactory(member=self.member)
        data = generate_post_form_data()

        self.client.login(username=self.member.user.username, password='password')
        response = self.client.post(reverse('blog.edit_post', kwargs={'id': post.id}), data)
        self.assertEqual(response.status_code, 302)

        edited_post = Post.objects.get(id=post.id)
        self.assertEqual(edited_post.text_call, data['text_call'])
        self.assertEqual(edited_post.title, data['title'])
        self.assertEqual(edited_post.text_content, data['text_content'])
        self.assertEqual(edited_post.member, self.member)

    def test_post_should_be_deleted_by_author(self):
        post = PostFactory(member=self.member)

        self.client.login(username=self.member.user.username, password='password')
        response = self.client.post(reverse('blog.delete_post'), {'id': post.id})
        self.assertEqual(response.status_code, 200)

    def test_post_should_be_deleted_by_pet_member(self):
        pet_member = MemberFactory(pet=self.member.pet)
        post = PostFactory(member=self.member)

        self.client.login(username=pet_member.user.username, password='password')
        response = self.client.post(reverse('blog.delete_post'), {'id': post.id})
        self.assertEqual(response.status_code, 200)

    def test_post_should_not_be_deleted_by_other_pet_member(self):
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
