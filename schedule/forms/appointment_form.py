import datetime as dt
from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from schedule.models import Appointment, Procedure
from schedule.validators import AppointmentValidator


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(lambda: [])
        self.fields['procedure'].queryset = Procedure.objects.all()
        booked_appointments = Appointment.objects.all().order_by(
            'date', 'time').values_list('date', 'time')
        today = dt.date.today()
        first_date, first_time = booked_appointments[0]
        # print(type(unavailable_dates[0]))
        # print(*unavailable_dates)
        unavailable_times = Appointment.objects.filter(
            date=first_date).values_list('time', flat=True)
        unavailable_times = {t.strftime('%H:%M') for t in unavailable_times}
        date_choices = [
            (today + dt.timedelta(days=i)).isoformat() for i in range(1, 61)
        ]
        time_choices = [
            (f'{i:02d}:00', f'{i:02d}:00') for i in range(8, 18)
            if f'{i:02d}:00' not in unavailable_times
        ]
        date_choices = [
            (date_choice, date_choice)
            for date_choice in date_choices
            if dt.date.fromisoformat(date_choice).weekday() != 6
        ]
        self.fields['date'].widget.choices = date_choices
        self.fields['time'].widget.choices = time_choices

    class Meta:
        model = Appointment
        fields = ('procedure', 'date', 'time')
        widgets = {
            'date': forms.Select,
            'time': forms.Select,
            'procedure': forms.Select,
        }

    def clean(self):
        cleaned_data = super().clean()
        AppointmentValidator(
            self.cleaned_data, self.fields, ErrorClass=ValidationError
        )
        return cleaned_data
