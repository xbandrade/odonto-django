from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import translation


class UserLoginTest(TestCase):
    def test_user_cannot_access_login_page_if_logged_in(self):
        with translation.override('en'):
            User.objects.create_user(username='my_user', password='my_pass')
            self.client.login(username='my_user', password='my_pass')
            response = self.client.get(
                reverse('users:login'),
                follow=True,
            )
            self.assertTemplateNotUsed(response, 'users/pages/login.html')
            self.assertTemplateUsed(response, 'users/pages/dashboard.html')

    def test_user_cannot_access_register_page_if_logged_in(self):
        with translation.override('en'):
            User.objects.create_user(username='my_user', password='my_pass')
            self.client.login(username='my_user', password='my_pass')
            response = self.client.get(
                reverse('users:register'),
                follow=True,
            )
            self.assertTemplateNotUsed(response, 'users/pages/register.html')
            self.assertTemplateUsed(response, 'users/pages/dashboard.html')

    def test_successful_login_redirects_to_user_dashboard(self):
        with translation.override('en'):
            user = User.objects.create_user(
                username='my_user', password='my_pass')
            response = self.client.post(
                reverse('users:login_create'),
                data={
                    'username': user.username,
                    'password': 'my_pass',
                },
                follow=True,
            )
            self.assertTemplateUsed(response, 'users/pages/dashboard.html')
