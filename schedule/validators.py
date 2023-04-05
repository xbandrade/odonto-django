from collections import defaultdict

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from schedule.models import Appointment


class AppointmentValidator:
    def __init__(self, data, fields, errors=None, ErrorClass=None):
        self.errors = errors or defaultdict(lambda: [])
        self.ErrorClass = ErrorClass or ValidationError
        self.data = data
        self.fields = fields
        self.clean()

    def clean(self, *args, **kwargs):
        cleaned_data = self.data
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        if Appointment.objects.filter(date=date, time=time).first():
            self.errors['date'].append(
                _('An appointment at this date and time '
                  'has already been booked!')
            )
            self.errors['time'].append(
                _('An appointment at this date and time '
                  'has already been booked!')
            )
        date_str = date.isoformat()
        time_str = time.strftime('%H:%M')
        unavailable_times = Appointment.objects.filter(
            date=date_str).values_list('time', flat=True)
        unavailable_times = {t.strftime('%H:%M') for t in unavailable_times}
        time_choices = [
            t for i in range(8, 18)
            if (t := f'{i:02d}:00') not in unavailable_times
        ]
        if date_str and time_str:
            if date.weekday() == 6:
                self.errors['date'].append(_('Invalid date selected.'))
            if not time_choices:
                self.errors['date'].append(
                    _('No available times for this date.'))
            if time_str not in time_choices:
                self.errors['time'].append(_('Invalid time selected.'))
        if self.errors:
            raise self.ErrorClass(self.errors)
