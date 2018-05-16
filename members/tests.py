from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from factories.member_factory import *
from django.core.files.uploadedfile import SimpleUploadedFile
from members.forms import NewMemberForm, TutorForm, PersonalInfoForm
from faker import Faker


faker = Faker()


def personal_info_form_data(member):
    return {'name': member.name, 'email': member.user.email, 'old_email': member.user.email,
            'facebook_link': member.facebook_link, 'lattes_link': member.lattes_link, 'photo': member.photo}


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
                self.assertTrue(response.url.startswith('/staff/login'))
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
        form_data = {'username': faker.user_name(), 'name': faker.name(), 'email': faker.email(),
                     'password': 'password', 'role': self.roles['scholar'].id}
        for key in form_data:
            value = form_data.pop(key)
            self.failIf(NewMemberForm(form_data).is_valid())
            form_data[key] = value

    def test_member_should_be_added_to_request_user_pet(self):
        request_member = MemberFactory(role=self.roles['tutor'])
        self.client.login(username=request_member.user.username, password='password')

        form_data = ({'username': faker.user_name(), 'name': faker.name(), 'email': faker.email(),
                      'password': 'password', 'role': self.roles['scholar'].id})
        response = self.client.post(reverse('members.add_member'), form_data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.filter(username=form_data['username']).exists())
        new_member = User.objects.get(username=form_data['username']).member
        self.assertEqual(new_member.pet, request_member.pet)
        self.assertEqual(new_member.user.username, form_data['username'])
        self.assertEqual(new_member.name, form_data['name'])
        self.assertEqual(new_member.user.email, form_data['email'])
        self.assertEqual(new_member.role.id, form_data['role'])

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

        form_data = ({'username': faker.user_name(), 'name': faker.name(), 'email': faker.email(),
                      'password': 'password', 'pet': PetFactory().id})
        response = self.client.post(reverse('members.add_tutor'), form_data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.filter(username=form_data['username']).exists())
        member = User.objects.get(username=form_data['username']).member
        self.assertEqual(member.pet.id, form_data['pet'])
        self.assertEqual(member.user.username, form_data['username'])
        self.assertEqual(member.name, form_data['name'])
        self.assertEqual(member.user.email, form_data['email'])
        self.assertEqual(member.role.name, 'tutor')

    def test_all_tutors_json_format_and_content(self):
        request_member = MemberFactory(role=self.roles['admin'])
        self.client.login(username=request_member.user.username, password='password')

        MemberFactory.create_batch(5, role=self.roles['tutor'])
        response = self.client.get(reverse('members.all_tutors'))
        self.assertTrue('data' in response.json())
        self.assertEqual(5, len(response.json()['data']))
        for item in response.json()['data']:
            self.assertEqual(4, len(item))
            self.assertEqual(Member.objects.get(id=item[0]).role.name, 'tutor')

    def test_all_members_json_format_and_content(self):
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

    def test_only_admin_should_access_tutors_json(self):
        for key, value in self.roles.items():
            member = MemberFactory(role=value)
            self.client.login(username=member.user.username, password='password')
            response = self.client.post(reverse('members.all_tutors'))
            self.assertEqual(response.status_code, 200 if key in ['admin'] else 302)

    def test_only_admin_and_tutor_should_access_members_json(self):
        for key, value in self.roles.items():
            member = MemberFactory(role=value)
            self.client.login(username=member.user.username, password='password')
            response = self.client.post(reverse('members.all_members'))
            self.assertEqual(response.status_code, 200 if key in ['admin', 'tutor'] else 302)

    def test_login_should_be_required_to_edit_personal_info(self):
        response = self.client.get(reverse('members.edit_personal_info'))
        self.assertEqual(response.status_code, 302)

    def test_edit_personal_info_page_should_return_200(self):
        self.client.login(username=MemberFactory().user.username, password='password')
        response = self.client.get(reverse('members.edit_personal_info'))
        self.assertEqual(response.status_code, 200)

    def test_personal_info_form_should_be_loaded_with_user_data(self):
        member = MemberFactory()
        self.client.login(username=member.user.username, password='password')
        response = self.client.get(reverse('members.edit_personal_info'))
        form_data = personal_info_form_data(member)
        self.assertEqual(form_data, response.context['form'].initial)

    def test_edit_member_page_should_return_404(self):
        self.client.login(username=MemberFactory(role=self.roles['admin']).user.username, password='password')
        response = self.client.get(reverse('members.edit_member', kwargs={'username': '0'}))
        self.assertTrue(response.status_code, 404)

    def test_only_admin_and_tutor_should_edit_member(self):
        response = self.client.get(reverse('members.edit_member', kwargs={'username': MemberFactory().user.username}))
        self.assertTrue(response.status_code, 302)
        for role in self.roles:
            self.client.login(username=MemberFactory(role=self.roles[role]).user.username, password='password')
            response = self.client.get(reverse('members.edit_member', kwargs={
                                       'username': MemberFactory().user.username}))
            if role not in ['admin', 'tutor']:
                self.assertEqual(response.status_code, 302)

    def test_admin_should_be_able_to_edit_tutors_only(self):
        self.client.login(username=MemberFactory(role=self.roles['admin']).user.username, password='password')
        for role in self.roles:
            response = self.client.get(reverse('members.edit_member', kwargs={
                                       'username': MemberFactory(role=self.roles[role]).user.username}))
            if role == 'tutor':
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 302)

    def test_tutor_should_be_able_to_edit_only_pet_members(self):
        tutor = MemberFactory(role=self.roles['tutor'])
        self.client.login(username=tutor.user.username, password='password')
        response = self.client.get(reverse('members.edit_member', kwargs={
                                   'username': MemberFactory(pet=tutor.pet).user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('members.edit_member', kwargs={'username': MemberFactory().user.username}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('members.edit_member', kwargs={
                                   'username': MemberFactory(role=self.roles['admin']).user.username}))
        self.assertEqual(response.status_code, 302)
