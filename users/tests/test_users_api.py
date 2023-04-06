from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.mixins import ProfileMixin


class UsersAPIMixin(ProfileMixin):
    def get_auth_data(self, username='user', password='pass'):
        userdata = {
            'username': username,
            'password': password,
        }
        user = self.make_user(
            username=userdata.get('username'),
            password=userdata.get('password'),
        )
        response = self.client.post(
            reverse('users:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }


class UsersAPITest(APITestCase, UsersAPIMixin):
    def test_users_api_returns_status_code_401_if_not_authenticated(self):
        url = reverse('users:user-api-list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_users_api_logged_user_can_retrieve_their_own_data(self):
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        id = auth_data.get('user').id
        url = reverse('users:user-api-detail', args=(id,))
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_users_api_logged_user_cannot_retrieve_someone_elses_data(self):
        another_user = self.make_another_user()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        id = another_user.id
        url = reverse('users:user-api-detail', args=(id,))
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )