from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import translation


class UserLogoutTest(TestCase):
    def test_user_cannot_logout_using_get_method(self):
        with translation.override('en'):
            User.objects.create_user(username='my_user', password='my_pass')
            self.client.login(username='my_user', password='my_pass')
            response = self.client.get(
                reverse('users:logout'),
                follow=True,
            )
            self.assertIn(
                'Invalid logout request',
                response.content.decode('utf-8')
            )

    def test_user_cannot_logout_another_user(self):
        with translation.override('en'):
            User.objects.create_user(username='my_user', password='my_pass')
            self.client.login(username='my_user', password='my_pass')
            response = self.client.post(
                reverse('users:logout'),
                follow=True,
                data={
                    'username': 'another_user'
                },
            )
            self.assertIn(
                'Invalid logout user',
                response.content.decode('utf-8')
            )

    def test_user_can_logout_successfully(self):
        with translation.override('en'):
            User.objects.create_user(username='my_user', password='my_pass')
            self.client.login(username='my_user', password='my_pass')
            response = self.client.post(
                reverse('users:logout'),
                follow=True,
                data={
                    'username': 'my_user'
                },
            )
            self.assertIn(
                'Logged out successfully',
                response.content.decode('utf-8')
            )
