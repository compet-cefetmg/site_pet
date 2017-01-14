from django.test import TestCase
from factories.auth_factory import *
from factories.member_factory import *


class LoginTestCase(TestCase):

    def setUp(self):
        self.roles = {}
        for role in ['admin', 'tutor', 'scholar', 'volunteer', 'contributor', 'ex-member']:
            self.roles[role] = MemberRoleFactory(name=role)
        self.tutor = MemberFactory(role=self.roles['tutor'])
        self.member = MemberFactory(role=self.roles['scholar'])

    def test_should_login_with_success_and_redirect(self):
        response = self.client.post('/staff/login', {'username': self.member.user.username, 'password': 'password'})
        self.assertEqual(response.status_code, 302)

    def test_should_not_login_and_reload_page(self):
        response = self.client.post('/staff/login', {'username': self.member.user.username, 'password': 'pwd'})
        self.assertEqual(response.status_code, 401)

    def test_should_logout_with_success(self):
        response = self.client.get('/staff/logout')
        self.assertEqual(response.status_code, 302)
