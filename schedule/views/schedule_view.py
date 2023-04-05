from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from schedule.forms.appointment_form import AppointmentForm
from utils.send_email import send_confirmation


class ScheduleView(View):
    template_name = 'schedule/pages/schedule.html'

    def get(self, request):
        form = AppointmentForm()
        curr_path = request.path
        context = {
            'curr_path': curr_path,
            'form': form,
        }
        return render(
            self.request,
            self.template_name,
            context
        )

    def post(self, request):
        form = AppointmentForm(request.POST or None)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.is_confirmed = False
            appointment.is_completed = False
            appointment.save()
            messages.success(
                request,
                _('Thank you for scheduling your appointment! You will '
                  'receive an email shortly to confirm your '
                  'appointment details.')
            )
            send_confirmation(appointment)
            return redirect(reverse('users:dashboard'))
        messages.error(request, _('Failed to book your appointment!'))
        return render(self.request, self.template_name)
