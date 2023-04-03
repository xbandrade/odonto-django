from django.test import TestCase

from tests.mixins import AppointmentMixin


class ScheduleViewTest(TestCase, AppointmentMixin):
    def setUp(self):
        super().setUp()
        self.appointment = self.make_appointment()

    def test_appointment_str_representation(self):
        needed_str = f"#{self.appointment.id} - {self.appointment.user.first_name}'s Appointment"  # noqa
        self.assertEqual(
            str(self.appointment), needed_str,
            msg=f"Appointment str representation must be '{needed_str}',"
                f" but '{self.appointment}' was received",
        )
