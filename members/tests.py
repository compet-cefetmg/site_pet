from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from factories.member_factory import *
from members.forms import NewMemberForm, TutorForm
from faker import Faker


faker = Faker()


class MemberTestCase(TestCase):

    def setUp(self):
        self.roles = {}
        for role in ['admin', 'tutor', 'scholar', 'volunteer', 'contributor', 'ex-member']:
            self.roles[role] = MemberRoleFactory(name=role)

    def test_index_page_should_return_200(self):
        response = self.client.get(reverse('members.index'))
        self.assertEqual(response.status_code, 200)

    def test_add_member_should_redirect_to_login_for_not_logged_user(self):
        response = self.client.get(reverse('members.add_member'))
        self.assertTrue(response.url.startswith('/staff/login'))
        self.assertEqual(response.status_code, 302)

    def test_add_member_should_redirect_to_login_for_wrong_role(self):
        for key, value in self.roles.items():
            if key != 'tutor':
                member = MemberFactory(role=value)
                self.client.login(username=member.user.username, password='password')
                response = self.client.post(reverse('members.add_member'))
                self.assertEqual(response.status_code, 302)

    def test_add_member_should_return_400_for_invalid_form(self):
        member = MemberFactory(role=self.roles['tutor'])
        self.client.login(username=member.user.username, password='password')
        response = self.client.post(reverse('members.add_member'))
        self.assertEqual(response.status_code, 400)

    def test_add_member_form_should_return_200(self):
        member = MemberFactory(role=self.roles['tutor'])
        self.client.login(username=member.user.username, password='password')
        response = self.client.get(reverse('members.add_member'))
        self.assertEqual(response.status_code, 200)

    def test_new_member_form_should_be_valid(self):
        form = NewMemberForm({'username': faker.user_name(), 'name': faker.name(), 'email': faker.email(),
                              'password': 'password', 'role': self.roles['scholar'].id})
        self.assertTrue(form.is_valid())

    def test_new_member_form_should_be_invalid(self):
        info = {'username': faker.user_name(), 'name': faker.name(), 'email': faker.email(),
                'password': 'password', 'role': self.roles['scholar'].id}
        for key in info:
            value = info.pop(key)
            self.failIf(NewMemberForm(info).is_valid())
            info[key] = value

    def test_member_should_be_added_to_request_user_pet(self):
        request_member = MemberFactory(role=self.roles['tutor'])
        self.client.login(username=request_member.user.username, password='password')

        info = ({'username': faker.user_name(), 'name': faker.name(), 'email': faker.email(),
                 'password': 'password', 'role': self.roles['scholar'].id})
        response = self.client.post(reverse('members.add_member'), info)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.filter(username=info['username']).exists())
        member = User.objects.get(username=info['username']).member
        self.assertEqual(member.pet, request_member.pet)
        self.assertEqual(member.user.username, info['username'])
        self.assertEqual(member.name, info['name'])
        self.assertEqual(member.user.email, info['email'])
        self.assertEqual(member.role.id, info['role'])

    def test_add_tutor_should_redirect_to_login_for_not_logged_user(self):
        response = self.client.get(reverse('members.add_tutor'))
        self.assertTrue(response.url.startswith('/staff/login'))
        self.assertEqual(response.status_code, 302)

    def test_add_tutor_should_redirect_to_login_for_wrong_role(self):
        for key, value in self.roles.items():
            if key != 'admin':
                member = MemberFactory(role=value)
                self.client.login(username=member.user.username, password='password')
                response = self.client.post(reverse('members.add_tutor'))
                self.assertEqual(response.status_code, 302)

    def test_tutor_form_should_be_valid(self):
        info = {'username': faker.user_name(), 'name': faker.name(), 'email': faker.email(),
                'password': 'password', 'pet': PetFactory().id}
        self.assertTrue(TutorForm(info).is_valid())

    def test_tutor_form_should_be_invalid(self):
        info = {'username': faker.user_name(), 'name': faker.name(), 'email': faker.email(),
                'password': 'password', 'pet': PetFactory().id}
        for key in info:
            value = info.pop(key)
            self.failIf(TutorForm(info).is_valid())
            info[key] = value

    def test_tutor_should_be_created(self):
        request_member = MemberFactory(role=self.roles['admin'])
        self.client.login(username=request_member.user.username, password='password')

        info = ({'username': faker.user_name(), 'name': faker.name(), 'email': faker.email(),
                 'password': 'password', 'pet': PetFactory().id})
        response = self.client.post(reverse('members.add_tutor'), info)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.filter(username=info['username']).exists())
        member = User.objects.get(username=info['username']).member
        self.assertEqual(member.pet.id, info['pet'])
        self.assertEqual(member.user.username, info['username'])
        self.assertEqual(member.name, info['name'])
        self.assertEqual(member.user.email, info['email'])
        self.assertEqual(member.role.name, 'tutor')

    def test_all_tutors_json(self):
        request_member = MemberFactory(role=self.roles['admin'])
        self.client.login(username=request_member.user.username, password='password')
        
        MemberFactory.create_batch(5, role=self.roles['tutor'])
        response = self.client.get(reverse('members.all_tutors'))
        self.assertTrue('data' in response.json())
        self.assertEqual(5, len(response.json()['data']))
        for item in response.json()['data']:
            self.assertEqual(4, len(item))
            self.assertEqual(Member.objects.get(id=item[0]).role.name, 'tutor')

    def test_all_members_json(self):
        request_member = MemberFactory(role=self.roles['tutor'])
        self.client.login(username=request_member.user.username, password='password')
        
        MemberFactory.create_batch(5, pet=request_member.pet)
        MemberFactory.create_batch(5)
        response = self.client.get(reverse('members.all_members'))
        self.assertTrue('data' in response.json())
        self.assertEqual(6, len(response.json()['data']))
        for item in response.json()['data']:
            self.assertEqual(5, len(item))
            self.assertEqual(Member.objects.get(id=item[0]).pet, request_member.pet)
