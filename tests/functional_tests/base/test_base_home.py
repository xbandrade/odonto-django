import os
from unittest.mock import patch

import pytest
from django.test import override_settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ..base import BaseFunctionalTest


@pytest.mark.functional_test
class HomePageFunctionalTest(BaseFunctionalTest):
    def test_home_treatments_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element(By.CLASS_NAME, 'treatments')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse('base:treatments'))

    @pytest.mark.skip('schedule page')
    def test_home_schedule_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element(By.CLASS_NAME, 'schedule')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse('base:schedule'))

    def test_home_about_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element(By.CLASS_NAME, 'about')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse('base:about'))

    @pytest.mark.skip('login page')
    def test_home_login_button_leads_to_correct_page(self):
        self.browser.get(self.live_server_url)
        button = self.browser.find_element(By.CLASS_NAME, 'login')
        button.click()
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse('base:login'))
