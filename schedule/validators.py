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
                _('An appointment at this time has already been booked!')
            )
            self.errors['time'].append(
                _('An appointment at this time has already been booked!')
            )
        date_str = date.isoformat()
        time_str = time.strftime('%H:%M')
        if date_str and time_str:
            if (date_str, date_str) not in self.fields['date'].widget.choices:
                self.errors['date'].append(_('Invalid date selected.'))
            if (time_str, time_str) not in self.fields['time'].widget.choices:
                self.errors['time'].append(_('Invalid time selected.'))
        if self.errors:
            raise self.ErrorClass(self.errors)
