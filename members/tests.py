from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from factories.member_factory import MemberFactory
from factories.auth_factory import *


class MemberTestCase(TestCase):

    def setUp(self):
        self.admin_group = AdminGroupFactory()
        self.tutors_group = TutorsGroupFactory()
        self.members_group = MembersGroupFactory()
    
    def test_index_page_should_return_200(self):
        response = self.client.get(reverse('members.index'))
        self.assertEqual(response.status_code, 200)

    def test_page_should_redirect_to_login(self):
        response = self.client.get(reverse('members.add_member'))
        self.assertTrue(response.url.startswith('/staff/login'))
        self.assertEqual(response.status_code, 302)

    def test_add_member_form_should_return_403(self):
        member = MemberFactory()
        member.user.groups.add(self.members_group)
        self.client.login(username=member.user.username, password='password')
        response = self.client.get(reverse('members.add_member'))
        self.assertEqual(response.status_code, 403)  

    def test_add_member_form_should_return_200(self):
        member = MemberFactory()
        member.user.groups.add(self.tutors_group)
        self.client.login(username=member.user.username, password='password')
        response = self.client.get(reverse('members.add_member'))
        self.assertEqual(response.status_code, 200)
