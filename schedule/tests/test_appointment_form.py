import datetime as dt

from django.test import TestCase
from django.utils import translation

from schedule.forms.appointment_form import AppointmentForm
from tests.mixins import AppointmentMixin


class AppointmentFormTest(TestCase, AppointmentMixin):
    def setUp(self):
        super().setUp()
        self.appointment = self.make_appointment()

    def test_user_can_schedule_if_date_and_time_are_available(self):
        with translation.override('en'):
            form_data = {
                'procedure': self.appointment.procedure,
                'date': self.appointment.date,
                'time': '15:00',
            }
            form = AppointmentForm(data=form_data)
            self.assertTrue(form.is_valid())
            self.assertNotIn('date', form.errors)
            self.assertNotIn('time', form.errors)

    def test_user_cannot_schedule_if_date_and_time_are_not_available(self):
        with translation.override('en'):
            form_data = {
                'procedure': self.appointment.procedure,
                'date': self.appointment.date,
                'time': self.appointment.time,
            }
            form = AppointmentForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('An appointment at this time has '
                          'already been booked!',
                          form.errors['date'])
            self.assertIn('An appointment at this time has '
                          'already been booked!',
                          form.errors['time'])

    def test_user_cannot_schedule_an_appointment_for_sunday(self):
        with translation.override('en'):
            for i in range(1, 8):
                next_sunday = self.today + dt.timedelta(days=i)
                if next_sunday.weekday() == 6:
                    break
            form_data = {
                'procedure': self.appointment.procedure,
                'date': next_sunday,
                'time': '13:00',
            }
            form = AppointmentForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('Invalid date selected.',
                          form.errors['date'])

    def test_user_cannot_schedule_an_appointment_out_of_time_range(self):
        with translation.override('en'):
            for i in range(1, 8):
                next_monday = self.today + dt.timedelta(days=i)
                if next_monday.weekday() == 0:
                    break
            form_data = {
                'procedure': self.appointment.procedure,
                'date': next_monday,
                'time': '23:00',
            }
            form = AppointmentForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('Invalid time selected.',
                          form.errors['time'])
