from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View

from schedule.models import Appointment


class AppointmentConfirmationView(View):
    template_name = 'schedule/pages/confirmation.html'

    def get(self, request, token):
        try:
            appointment = Appointment.objects.get(confirmation_token=token)
        except (Appointment.DoesNotExist, ValidationError):
            appointment = None
        curr_path = request.path
        context = {
            'curr_path': curr_path,
        }
        if not appointment:
            context['invalid'] = True
        elif not appointment.is_confirmed:
            context['already_confirmed'] = False
            appointment.is_confirmed = True
            appointment.save()
        else:
            context['already_confirmed'] = True
        return render(
            self.request,
            self.template_name,
            context
        )
