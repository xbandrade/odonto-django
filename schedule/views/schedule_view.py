import datetime as dt

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from schedule.forms.appointment_form import AppointmentForm
from schedule.models import Appointment


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
            messages.success(request, _('Appointment booked successfully!'))
            return redirect(reverse('users:dashboard'))
        messages.error(request, _('Failed to book your appointment!'))
        return render(self.request, self.template_name)


class AvailableAppointmentTimes(View):
    def get(self, request):
        selected_date = request.GET.get('date')
        booked_appointments = Appointment.objects.filter(
            date=selected_date).values_list('time', flat=True)
        all_times = [f'{i:02d}:00' for i in range(8, 18)]
        available_times = [
            time for time in all_times if time not in booked_appointments
        ]
        print(*available_times)
        return JsonResponse({'available_times': available_times})


class AvailableAppointmentDates(View):
    def get(self, request):
        selected_time = request.GET.get('time')
        booked_appointments = Appointment.objects.filter(
            time=selected_time).values_list('date', flat=True)
        today = dt.date.today()
        all_dates = [
            (today + dt.timedelta(days=i)).isoformat() for i in range(1, 61)
            if (today + dt.timedelta(days=i)).weekday() != 6
        ]
        available_dates = [
            date for date in all_dates if date not in booked_appointments
        ]
        print(*available_dates)
        return JsonResponse({'available_dates': available_dates})
