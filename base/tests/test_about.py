from django.test import TestCase
from django.urls import resolve, reverse

from base import views


class BaseAboutViewTest(TestCase):
    def test_base_about_view_is_correct(self):
        view = resolve(reverse('base:about'))
        self.assertIs(view.func.view_class, views.AboutView)

    def test_base_about_view_returns_status_200(self):
        response = self.client.get(reverse('base:about'))
        self.assertEqual(response.status_code, 200)

    def test_base_about_view_loads_correct_template(self):
        response = self.client.get(reverse('base:about'))
        self.assertTemplateUsed(response, 'global/pages/about.html')
