from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'admin@admin.com', 'password')


    def test_post_should_return_unauthorized(self):
        response = self.client.get(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 302)


    def test_post_form_should_be_loaded(self):
        self.client.login(username='admin', password='password')
        self.assertTrue(self.user.is_authenticated())
        response = self.client.get(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 200)


    def test_post_should_not_be_created(self):
        self.client.login(username='admin', password='password')
        self.assertTrue(self.user.is_authenticated())
        response = self.client.post(reverse('blog.add_post'))
        self.assertEqual(response.status_code, 400)
