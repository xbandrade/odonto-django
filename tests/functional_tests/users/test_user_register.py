import pytest
from django.utils import translation
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.base import BaseFunctionalTest


@pytest.mark.functional_test
class UserRegisterTest(BaseFunctionalTest):
    def get_form(self):
        return self.browser.find_element(
            By.CLASS_NAME,
            'main-form'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/users/register/')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')
        callback(form)
        return form

    def test_first_name_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                first_name_field = self.get_by_placeholder(
                    form, 'Enter your first name'
                )
                first_name_field.click()
                first_name_field.send_keys('  ')
                first_name_field.send_keys(Keys.ENTER)
                form = self.get_form()
                self.assertIn('First name cannot be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_last_name_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                last_name_field = self.get_by_placeholder(
                    form, 'Enter your last name'
                )
                last_name_field.send_keys(' ')
                last_name_field.send_keys(Keys.ENTER)
                form = self.get_form()
                self.assertIn('Last name cannot be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_username_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                username_field = self.get_by_placeholder(
                    form, 'Enter a username'
                )
                username_field.send_keys(' ')
                username_field.send_keys(Keys.ENTER)
                form = self.get_form()
                self.assertIn('Username is required', form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            with translation.override('en'):
                password1 = self.get_by_placeholder(
                    form, 'Enter your password'
                )
                password2 = self.get_by_placeholder(
                    form, 'Enter your password again'
                )
                password1.send_keys('P@ssw0rd')
                password2.send_keys('P@ssw0rd_different')
                password2.send_keys(Keys.ENTER)
                form = self.get_form()
                self.assertIn('Passwords must match', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_success(self):
        with translation.override('en'):
            self.browser.get(self.live_server_url + '/users/register/')
            form = self.get_form()
            self.get_by_placeholder(
                form, 'Enter your first name'
            ).send_keys('First')
            self.get_by_placeholder(
                form, 'Enter your last name'
            ).send_keys('Last')
            self.get_by_placeholder(
                form, 'Enter a username'
            ).send_keys('firstlast')
            self.get_by_placeholder(
                form, 'email@address.com'
            ).send_keys('first@last.com')
            self.get_by_placeholder(
                form, 'Enter your password'
            ).send_keys('P@ssw0rd')
            self.get_by_placeholder(
                form, 'Enter your password again'
            ).send_keys('P@ssw0rd')
            self.get_by_placeholder(
                form, '12345678909'
            ).send_keys('12345678909')
            form.submit()
            self.assertIn(
                'User has been created, please log in',
                self.browser.find_element(By.TAG_NAME, 'body').text
            )
