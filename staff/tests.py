from django.test import TestCase
from factories.auth_factory import *
from factories.member_factory import MemberFactory


class LoginTestCase(TestCase):

    def setUp(self):
        AdminGroupFactory()
        self.tutor = MemberFactory()
        self.member = MemberFactory()
        self.tutor.user.groups.add(TutorsGroupFactory())
        self.member.user.groups.add(MembersGroupFactory())

    def test_should_login_with_success_and_redirect(self):
        response = self.client.post('/staff/login', {'username': self.member.user.username, 'password': 'password'})
        self.assertEqual(response.status_code, 302)

    def test_should_not_login_and_reload_page(self):
        response = self.client.post('/staff/login', {'username': self.member.user.username, 'password': 'pwd'})
        self.assertEqual(response.status_code, 401)

    def test_should_logout_with_success(self):
        response = self.client.get('/staff/logout')
        self.assertEqual(response.status_code, 302)
