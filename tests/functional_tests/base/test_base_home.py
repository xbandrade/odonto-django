import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional_tests.base import BaseFunctionalTest


@pytest.mark.functional_test
class HomePageFunctionalTest(BaseFunctionalTest):
    def test_home_services_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element(By.CLASS_NAME, 'services')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse('base:services'))

    def test_home_schedule_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element(By.CLASS_NAME, 'schedule')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse('schedule:schedule'))

    def test_home_about_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element(By.CLASS_NAME, 'about')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse('base:about'))

    def test_home_login_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element(By.CLASS_NAME, 'login')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse('users:login'))

    def test_home_register_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element(By.CLASS_NAME, 'register')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse('users:register'))
