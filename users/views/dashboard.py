from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from schedule.models import Appointment


class UserDashboardView(LoginRequiredMixin, View):
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get(self, request):
        appointments = Appointment.objects.filter(
            user=request.user, is_completed=False).order_by('date', 'time')
        context = {
            'appointments': appointments,
        }
        return render(request, 'users/pages/dashboard.html', context=context)
