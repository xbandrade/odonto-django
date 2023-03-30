import os

from django.test import TestCase
from django.urls import resolve, reverse

from base import views


class BaseTreatmentsViewTest(TestCase):
    def test_base_treatments_view_is_correct(self):
        view = resolve(reverse('base:treatments'))
        self.assertIs(view.func.view_class, views.TreatmentsView)

    def test_base_treatments_view_returns_status_200(self):
        response = self.client.get(reverse('base:treatments'))
        self.assertEqual(response.status_code, 200)

    def test_base_treatments_view_loads_correct_template(self):
        response = self.client.get(reverse('base:treatments'))
        self.assertTemplateUsed(response, 'global/pages/treatments.html')
