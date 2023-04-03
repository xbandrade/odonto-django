from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from schedule.models import Appointment


class UserDashboardView(LoginRequiredMixin, View):
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_appointment(self, id=None):
        appointment = None
        if id:
            appointment = Appointment.objects.filter(
                is_completed=False,
                user=self.request.user,
                id=id,
            ).first()
            if not appointment:
                raise Http404()
        return appointment

    def get(self, request):
        appointments = Appointment.objects.filter(
            user=request.user, is_completed=False).order_by('date', 'time')
        closed_appointments = Appointment.objects.filter(
            user=request.user, is_completed=True).order_by('date', 'time')
        context = {
            'appointments': appointments,
            'closed_appointments': closed_appointments,
        }
        return render(request, 'users/pages/dashboard.html', context=context)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardAppointmentDelete(UserDashboardView):
    def post(self, *args, **kwargs):
        appointment = self.get_appointment(self.request.POST.get('id'))
        appointment.delete()
        messages.success(self.request, _('Appointment successfully deleted'))
        return redirect(reverse('users:dashboard'))
