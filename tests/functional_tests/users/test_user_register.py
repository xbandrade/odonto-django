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

    def fill_form_valid_data(self,
                             form,
                             first='First',
                             last='Last',
                             username='firstlast',
                             email='first@last.com',
                             password='P@ssw0rd',
                             cpf='12345678909',
                             phone_number=2499912345):
        self.get_by_placeholder(
            form, 'Enter your first name'
        ).send_keys(first)
        self.get_by_placeholder(
            form, 'Enter your last name'
        ).send_keys(last)
        self.get_by_placeholder(
            form, 'Enter a username'
        ).send_keys(username)
        self.get_by_placeholder(
            form, 'email@address.com'
        ).send_keys(email)
        self.get_by_placeholder(
            form, 'Enter your password'
        ).send_keys(password)
        self.get_by_placeholder(
            form, 'Enter your password again'
        ).send_keys(password)
        self.get_by_placeholder(
            form, '12345678909'
        ).send_keys(cpf)
        self.get_by_placeholder(
            form, '2499999999'
        ).send_keys(phone_number)

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

    def test_cpf_empty_error_message(self):
        def callback(form):
            with translation.override('en'):
                username_field = self.get_by_placeholder(
                    form, '12345678909'
                )
                username_field.send_keys(' ')
                username_field.send_keys(Keys.ENTER)
                form = self.get_form()
                self.assertIn('CPF is required', form.text)
        self.form_field_test_with_callback(callback)

    def test_cpf_cannot_have_less_than_11_characters_long(self):
        def callback(form):
            with translation.override('en'):
                username_field = self.get_by_placeholder(
                    form, '12345678909'
                )
                username_field.send_keys('123456')
                username_field.send_keys(Keys.ENTER)
                form = self.get_form()
                self.assertIn('CPF must have 11 digits', form.text)
        self.form_field_test_with_callback(callback)

    def test_cpf_cannot_be_invalid(self):
        def callback(form):
            with translation.override('en'):
                username_field = self.get_by_placeholder(
                    form, '12345678909'
                )
                username_field.send_keys('12345678999')
                username_field.send_keys(Keys.ENTER)
                form = self.get_form()
                self.assertIn('CPF must be valid', form.text)
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
            self.fill_form_valid_data(form)
            form.submit()
            self.assertIn(
                'User has been created, please log in',
                self.browser.find_element(By.TAG_NAME, 'body').text
            )
