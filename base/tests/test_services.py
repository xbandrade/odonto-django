from django.test import TestCase
from django.urls import resolve, reverse

from base import views


class BaseServicesViewTest(TestCase):
    def test_base_services_view_is_correct(self):
        view = resolve(reverse('base:services'))
        self.assertIs(view.func.view_class, views.ServicesView)

    def test_base_services_view_returns_status_200(self):
        response = self.client.get(reverse('base:services'))
        self.assertEqual(response.status_code, 200)

    def test_base_services_view_loads_correct_template(self):
        response = self.client.get(reverse('base:services'))
        self.assertTemplateUsed(response, 'global/pages/services.html')
