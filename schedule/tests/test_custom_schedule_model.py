from django.test import TestCase

from tests.mixins.base_mixin import CustomScheduleMixin


class CustomScheduleModelTest(TestCase, CustomScheduleMixin):
    def setUp(self):
        super().setUp()
        self.appointment = self.custom_schedule()

    def test_appointment_str_representation(self):
        needed_str = f"#{self.appointment.id} - {self.appointment.user.first_name}'s Custom Appointment"  # noqa
        self.assertEqual(
            str(self.appointment), needed_str,
            msg=f"Appointment str representation must be '{needed_str}',"
                f" but '{self.appointment}' was received",
        )
