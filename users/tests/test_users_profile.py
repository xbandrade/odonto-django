from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tests.mixins import AppointmentMixin, ProfileMixin
from users.forms import RegisterForm
from users.models import Profile


class UserProfileTest(TestCase, ProfileMixin):
    def test_profile_extra_info_goes_to_user_correctly(self):
        user = self.make_user(cpf='82940462054', phone_number='2199999998')
        self.assertEquals(user.profile.cpf, '82940462054')
        self.assertEquals(user.profile.phone_number, '2199999998')
