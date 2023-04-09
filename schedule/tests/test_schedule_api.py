from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.mixins import AppointmentMixin


class ScheduleAPIMixin(AppointmentMixin):
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


class ScheduleAPITest(APITestCase, ScheduleAPIMixin):
    def test_schedule_api_returns_status_code_401_if_not_authenticated(self):
        url = reverse('schedule:schedule-api-list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_schedule_api_logged_user_can_retrieve_own_appointments(self):
        auth_data = self.get_auth_data()
        user = auth_data.get('user')
        self.make_appointments_in_batch(
            user_data=user,
            datetime_list=[
                ('', '12:00'),
                ('', '13:00'),
                ('', '14:00'),
                ('', '15:00'),
                ('', '16:00'),
            ]
        )
        jwt_access_token = auth_data.get('jwt_access_token')
        url = reverse('schedule:schedule-api-list')
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_schedule_api_logged_user_can_retrieve_a_single_appointment(self):
        auth_data = self.get_auth_data()
        user = auth_data.get('user')
        appointment = self.make_appointment(user_data=user)
        jwt_access_token = auth_data.get('jwt_access_token')
        url = reverse('schedule:schedule-api-detail', args=(appointment.id,))
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), appointment.id)

    def test_schedule_api_logged_user_cannot_retrieve_someone_elses_data(self):
        another_user = self.make_another_user()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        id = another_user.id
        url_details = reverse('users:user-api-detail', args=(id,))
        response = self.client.get(
            url_details,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_schedule_api_user_cannot_schedule_if_not_authenticated(self):
        form_data = self.get_appointment_form()
        url = reverse('schedule:schedule-api-list')
        response = self.client.post(url, data=form_data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_schedule_api_user_can_schedule_if_authenticated(self):
        auth_data = self.get_auth_data()
        user = auth_data.get('user')
        jwt_access_token = auth_data.get('jwt_access_token')
        form_data = self.get_appointment_form(user)
        url = reverse('schedule:schedule-api-list')
        response = self.client.post(
            url,
            data=form_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_schedule_api_user_cannot_schedule_for_someone_else(self):
        another_user = self.make_another_user()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        form_data = self.get_appointment_form(another_user)
        url = reverse('schedule:schedule-api-list')
        response = self.client.post(
            url,
            data=form_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
