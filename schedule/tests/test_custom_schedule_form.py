from django.test import TestCase
from django.utils import translation

from schedule.forms import CustomScheduleForm
from tests.mixins import CustomScheduleMixin


class CustomScheduleFormTest(TestCase, CustomScheduleMixin):
    def setUp(self):
        super().setUp()
        self.custom_appointment = self.custom_schedule()

    def test_user_can_request_custom_schedule_if_form_is_valid(self):
        with translation.override('en'):
            form_data = self.get_form_data(self.custom_appointment)
            form = CustomScheduleForm(data=form_data)
            self.assertTrue(form.is_valid())
            self.assertFalse(form.errors)

    def test_user_cannot_request_custom_schedule_if_fields_are_empty(self):
        with translation.override('en'):
            form_data = {
                'procedure': '    ',
                'date': '    ',
                'time': '    ',
                'details': '    '
            }
            form = CustomScheduleForm(data=form_data)
            expected_errors = {
                'procedure': ['This field is required.'],
                'date': ['This field is required.'],
                'time': ['This field is required.'],
                'details': ['This field is required.'],
            }
            self.assertFalse(form.is_valid())
            self.assertDictEqual(form.errors, expected_errors)
