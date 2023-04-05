from django.test import TestCase
from django.urls import resolve, reverse

from schedule import views


class CustomScheduleViewTest(TestCase):
    def test_custom_schedule_view_is_correct(self):
        view = resolve(reverse('schedule:custom'))
        self.assertIs(view.func.view_class, views.CustomScheduleView)

    def test_custom_schedule_view_returns_status_200(self):
        response = self.client.get(reverse('schedule:custom'))
        self.assertEqual(response.status_code, 200)

    def test_custom_schedule_takes_to_correct_page(self):
        response = self.client.get(reverse('schedule:custom'))
        self.assertTemplateUsed(
            response, 'schedule/pages/custom_schedule.html')
