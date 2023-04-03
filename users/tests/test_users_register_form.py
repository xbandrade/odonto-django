from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from django.utils import translation
from parameterized import parameterized

from users.forms import RegisterForm


class UserRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Enter your first name'),
        ('last_name', 'Enter your last name'),
        ('email', 'email@address.com'),
        ('cpf', '12345678909'),
        ('phone_number', '2499999999'),
        ('password', 'Enter your password'),
        ('password2', 'Enter your password again'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        with translation.override('en'):
            form = RegisterForm()
            current = form[field].field.widget.attrs['placeholder']
            self.assertEqual(current, placeholder)

    @parameterized.expand([
        ('email',  'Enter a valid email'),
        ('password', (
            'Password must contain at least one uppercase character, '
            'one lowercase character and one number. The length should be '
            'at least 8 characters.'
        )),
        ('cpf', 'Enter a valid CPF'),
    ])
    def test_fields_help_text(self, field, needed):
        with translation.override('en'):
            form = RegisterForm()
            current = form[field].field.help_text
            self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('password2', 'Repeat Password'),
        ('cpf', 'CPF'),
        ('phone_number', 'Phone Number'),
    ])
    def test_fields_label(self, field, needed):
        with translation.override('en'):
            form = RegisterForm()
            current = form[field].field.label
            self.assertEqual(current, needed)


class UserRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'first_name': 'First',
            'last_name': 'Last',
            'username': 'testuser',
            'email': 'email@email.com',
            'password': 'Str0ngPa$$word',
            'password2': 'Str0ngPa$$word',
            'cpf': '00000012360',
            'phone_number': 2499991234
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Username is required'),
        ('first_name', 'First name cannot be empty'),
        ('last_name', 'Last name cannot be empty'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please repeat your password'),
        ('email', 'Email is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        with translation.override('en'):
            self.form_data[field] = ''
            url = reverse('users:create')
            response = self.client.post(url, data=self.form_data, follow=True)
            self.assertIn(msg, response.content.decode('utf-8'))
            self.assertIn(msg, response.context['form'].errors.get(field))

    def test_password_field_has_lower_upper_case_and_numbers(self):
        msg = (
            'Password must contain at least an uppercase character, a '
            'lowercase character, a number and be at least 8 characters long.'
        )
        self.form_data['password'] = '123q'
        url = reverse('users:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@ABC123qQ'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_password_and_password_confirmation_match(self):
        self.form_data['password'] = '@ABC123qQ'
        self.form_data['password2'] = '@ABCl23qD'
        url = reverse('users:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Passwords must match'
        self.assertIn(msg, response.context['form'].errors.get('password2'))
        self.assertIn(msg, response.content.decode('utf-8'))
        self.form_data['password'] = '@ABC123qQ'
        self.form_data['password2'] = '@ABC123qQ'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_return_404(self):
        url = reverse('users:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        with translation.override('en'):
            msg = 'User email is already in use'
            url = reverse('users:create')
            self.client.post(url, data=self.form_data, follow=True)
            response = self.client.post(url, data=self.form_data, follow=True)
            self.assertIn(msg, response.context['form'].errors.get('email'))
            self.assertIn(msg, response.content.decode('utf-8'))

    def test_cpf_field_must_be_unique(self):
        with translation.override('en'):
            msg = 'This CPF is already registered'
            url = reverse('users:create')
            self.client.post(url, data=self.form_data, follow=True)
            response = self.client.post(url, data=self.form_data, follow=True)
            self.assertIn(msg, response.context['form'].errors.get('cpf'))
            self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_min_length_should_be_4(self):
        with translation.override('en'):
            msg = 'Username must have at least 4 characters'
            self.form_data['username'] = 'joa'
            url = reverse('users:create')
            response = self.client.post(url, data=self.form_data, follow=True)
            self.assertIn(msg, response.content.decode('utf-8'))
            self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        with translation.override('en'):
            msg = 'Username must have 150 characters or less'
            self.form_data['username'] = 'a' * 151
            url = reverse('users:create')
            response = self.client.post(url, data=self.form_data, follow=True)
            self.assertIn(msg, response.content.decode('utf-8'))
            self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_cannot_be_admin(self):
        with translation.override('en'):
            msg = 'Forbidden username'
            self.form_data['username'] = 'admin'
            url = reverse('users:create')
            response = self.client.post(url, data=self.form_data, follow=True)
            self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_created_user_can_login(self):
        url = reverse('users:create')
        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password2': '@Bc123456',
        })
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc123456'
        )
        self.assertTrue(is_authenticated)
