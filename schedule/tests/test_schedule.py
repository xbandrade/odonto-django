from django.test import TestCase
from django.urls import resolve, reverse

from schedule import views


class ScheduleViewTest(TestCase):
    def test_schedule_view_is_correct(self):
        view = resolve(reverse('schedule:schedule'))
        self.assertIs(view.func.view_class, views.ScheduleView)

    def test_schedule_view_returns_status_200(self):
        response = self.client.get(reverse('schedule:schedule'))
        self.assertEqual(response.status_code, 200)

    def test_schedule_view_loads_correct_template(self):
        response = self.client.get(reverse('schedule:schedule'))
        self.assertTemplateUsed(response, 'schedule/pages/schedule.html')

    def test_custom_schedule_takes_to_correct_page(self):
        response = self.client.get(reverse('schedule:custom'))
        self.assertTemplateUsed(response, 'schedule/pages/custom.html')
