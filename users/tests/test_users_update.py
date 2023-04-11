from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework import status

from tests.mixins import ProfileMixin
from users import views


class UserUpdateViewTest(TestCase, ProfileMixin):
    def test_update_view_is_correct(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        view = resolve(reverse('users:update'))
        self.assertIs(view.func.view_class, views.UserUpdateView)

    def test_update_view_returns_status_200_if_user_is_logged_in(self):
        self.make_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        response = self.client.get(reverse('users:update'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_view_loads_correct_template(self):
        self.make_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        response = self.client.get(reverse('users:update'))
        self.assertTemplateUsed(response, 'users/pages/update.html')

    def test_user_must_login_to_update_their_information(self):
        response = self.client.get(reverse('users:update'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTemplateNotUsed(response, 'users/pages/update.html')

    def test_logged_in_user_can_update_their_own_information(self):
        user = self.make_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        updated_data = {
            'username': 'userupdated',
            'first_name': 'Updatedfirst',
            'last_name': 'Updatedlast'
        }
        response = self.client.post(
            reverse('users:update'),
            data=updated_data,
        )
        user.refresh_from_db()
        self.assertDictContainsSubset(updated_data, model_to_dict(user))
        self.assertRedirects(response, reverse(
            'users:dashboard'), status_code=302, target_status_code=200)


class UserPasswordChangeViewTest(TestCase, ProfileMixin):
    def test_password_change_view_is_correct(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        view = resolve(reverse('users:change_password'))
        self.assertIs(view.func.view_class, views.PasswordUpdateView)

    def test_password_change_view_returns_200_if_user_is_logged_in(self):
        self.make_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        response = self.client.get(reverse('users:change_password'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_must_login_to_change_their_password(self):
        response = self.client.get(reverse('users:change_password'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTemplateNotUsed(
            response, 'users/pages/change_password.html')

    def test_password_change_view_loads_correct_template(self):
        self.make_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        response = self.client.get(reverse('users:change_password'))
        self.assertTemplateUsed(response, 'users/pages/change_password.html')

    def test_user_can_successfully_change_their_own_password(self):
        user = self.make_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        updated_data = {
            'password': 'new_Passw0rd',
            'password2': 'new_Passw0rd'
        }
        response = self.client.post(
            reverse('users:change_password'),
            data=updated_data,
        )
        user.refresh_from_db()
        self.client.logout()
        self.client.login(username='my_user', password='new_Passw0rd')
        self.assertRedirects(response, reverse(
            'users:dashboard'), status_code=302, target_status_code=200)
