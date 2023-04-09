import datetime as dt

from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from schedule.models import Appointment


class AvailableAppointmentTimes(View):
    def get(self, request):
        selected_date = request.GET.get('date')
        booked_appointments = Appointment.objects.filter(
            date=selected_date).values_list('time', flat=True)
        booked_appointments = [apt.strftime('%H:%M')
                               for apt in booked_appointments]
        all_times = [f'{i:02d}:00' for i in range(8, 18)]
        available_times = [
            time for time in all_times if time not in booked_appointments
        ]
        return JsonResponse({'available_times': available_times})

    def get_url(self):
        return reverse('schedule:times')


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
        return JsonResponse({'available_dates': available_dates})

    def get_url(self):
        return reverse('schedule:dates')
