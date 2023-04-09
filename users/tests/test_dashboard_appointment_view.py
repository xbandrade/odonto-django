from django.test import TestCase
from django.urls import resolve, reverse

from tests.mixins import AppointmentMixin
from users import views
from users.models import User


class AppointmentViewTest(TestCase, AppointmentMixin):
    def setUp(self) -> None:
        super().setUp()
        user = User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')
        self.appointment = self.make_appointment(user_data=user)

    def test_appointment_view_is_correct(self):
        pk = self.appointment.id
        view = resolve(reverse('users:appointment_detail', args=(pk,)))
        self.assertIs(view.func.view_class, views.AppointmentDetailView)

    def test_appointment_view_returns_status_200(self):
        id = self.appointment.id
        response = self.client.get(
            reverse('users:appointment_detail',  args=(id,)))
        self.assertEqual(response.status_code, 200)

    def test_appointment_view_loads_correct_template(self):
        id = self.appointment.id
        response = self.client.get(
            reverse('users:appointment_detail',  args=(id,)))
        self.assertTemplateUsed(response, 'users/pages/appointment.html')
