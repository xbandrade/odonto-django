import datetime as dt

from django.contrib.auth.models import User

from schedule.models import Appointment, CustomSchedule, Procedure
from users.models import Profile


class ProfileMixin:
    def make_user(self,
                  first_name='User',
                  last_name='Name',
                  username='username',
                  password='P@Ssw0rd123',
                  email='user@usermail.com',
                  cpf='06174322017',
                  phone_number=''):
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )
        profile = Profile(user=user, cpf=cpf, phone_number=phone_number)
        profile.save()
        return user

    def make_another_user(self,
                          first_name='Second',
                          last_name='User',
                          username='newuser',
                          password='P@Ssw0rd123',
                          email='anotheruser@usermail.com',
                          cpf='40135148006',
                          phone_number=''):
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )
        profile = Profile(user=user, cpf=cpf, phone_number=phone_number)
        profile.save()
        return user

    def get_user_form_data(self, user):
        profile = user.profile
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'password': user.password,
            'email': user.email,
            'cpf': profile.cpf,
            'phone_number': profile.phone_number,
        }

    def create_user_data(self):
        return {
            'first_name': 'firstnametst',
            'last_name': 'lastnametst',
            'username': 'usernametst',
            'password': 'Pa$$w0rd',
            'password2': 'Pa$$w0rd',
            'email': 'testemail@emailtst.com',
            'cpf': '50135860709',
            'phone_number': '',
        }


class AppointmentMixin(ProfileMixin):
    appointment = None
    today = None

    def get_next_available_date(self):
        self.today = dt.date.today()
        date = self.today + dt.timedelta(days=8)
        if date.weekday() == 6:
            date += dt.timedelta(days=1)
        return date.isoformat()

    def make_procedure(self, name='Procedure', price=115.99):
        return Procedure.objects.create(name=name, name_pt=name, price=price)

    def make_appointment(self,
                         procedure_data=None,
                         user_data=None,
                         date='',
                         time='11:00'):
        if not procedure_data:
            procedure_data = {}
        if not user_data:
            user_data = self.make_user()
        if not date:
            date = self.get_next_available_date()
        return Appointment.objects.create(
            procedure=self.make_procedure(**procedure_data),
            user=user_data,
            date=date,
            time=time,
        )

    def make_appointments_in_batch(self, user_data, datetime_list):
        for date, time in datetime_list:
            self.make_appointment(user_data=user_data, date=date, time=time)

    def get_appointment_form(self, user=None, procedure=None):
        user = user or self.make_user()
        procedure = procedure or self.make_procedure('TestingProc')
        return {
            'user': user.id,
            'procedure': procedure.name,
            'date': self.get_next_available_date(),
            'time': '15:00',
        }


class CustomScheduleMixin(ProfileMixin):
    def custom_schedule(self,
                        user_data=None,
                        procedure='Custom Procedure',
                        date='22-08-2023',
                        time='16:00',
                        details='I need some custom treatments'):
        if not user_data:
            user_data = {}
        return CustomSchedule.objects.create(
            user=self.make_user(**user_data),
            procedure=procedure,
            date=date,
            time=time,
            details=details,
        )

    def get_form_data(self, custom_appointment):
        return {
            'procedure': custom_appointment.procedure,
            'date': custom_appointment.date,
            'time': custom_appointment.time,
            'details': custom_appointment.details,
        }
