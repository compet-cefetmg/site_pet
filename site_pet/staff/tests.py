from django.test import TestCase
from django.contrib.auth.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@admin.com', 'password')


    def test_should_login_with_success_and_redirect(self):
        response = self.client.post('/staff/login', {'username': 'admin', 'password': 'password'})
        self.assertEqual(response.status_code, 302)


    def test_should_not_login_and_reload_page(self):
        response = self.client.post('/staff/login', {'username': 'admin', 'password': 'pwd'})
        self.assertEqual(response.status_code, 401)


    def test_should_logout_with_success(self):
        response = self.client.get('/staff/logout')
        self.assertEqual(response.status_code, 302)

