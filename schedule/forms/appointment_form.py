import datetime as dt
from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from schedule.models import Appointment
from schedule.validators import AppointmentValidator


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(lambda: [])
        booked_appointments = Appointment.objects.values_list('date', 'time')
        booked_dates = [appointment[0] for appointment in booked_appointments]
        booked_times = [appointment[1] for appointment in booked_appointments]
        today = dt.date.today()
        date_choices = [
            (today + dt.timedelta(days=i)).isoformat() for i in range(1, 61)
        ]
        date_choices = [
            (date_choice, date_choice)
            for date_choice in date_choices
            if dt.date.fromisoformat(date_choice).weekday() != 6
        ]
        time_choices = [
            (f'{i:02d}:00', f'{i:02d}:00') for i in range(8, 18)
        ]
        self.fields['date'].widget.choices = date_choices
        self.fields['time'].widget.choices = time_choices

    class Meta:
        model = Appointment
        fields = ('procedure', 'date', 'time')
        widgets = {
            'date': forms.Select,
            'time': forms.Select,
        }

    def clean(self):
        cleaned_data = super().clean()
        AppointmentValidator(
            self.cleaned_data, self.fields, ErrorClass=ValidationError
        )
        return cleaned_data
