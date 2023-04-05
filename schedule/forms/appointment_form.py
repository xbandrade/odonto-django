import datetime as dt
from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from schedule.models import Appointment, Procedure
from schedule.validators import AppointmentValidator


class AppointmentForm(forms.ModelForm):
    price = forms.CharField(
        label=_('Price'),
        required=False,
        widget=forms.TextInput(attrs={'readonly': True, 'id': 'price'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(lambda: [])
        self.fields['procedure'].widget.choices = [
            (p.pk, p.name) for p in Procedure.objects.all()
        ]
        today = dt.date.today()
        date_choices = [
            (today + dt.timedelta(days=i)).isoformat() for i in range(1, 61)
        ]
        first_procedure = Procedure.objects.first().id
        price_str = '{:,.2f}'.format(
            Procedure.objects.first().price
        ).replace('.', ',')
        self.fields['procedure'].initial = first_procedure
        self.fields['procedure'].label = _('Select a procedure')
        self.fields['price'].initial = f'R$ {price_str}'
        unavailable_times = Appointment.objects.filter(
            date=date_choices[0]).values_list('time', flat=True)
        unavailable_times = {t.strftime('%H:%M') for t in unavailable_times}
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
        fields = ('procedure', 'price', 'date', 'time')
        widgets = {
            'procedure': forms.Select(attrs={
                'id': 'procedure',
            }),
            'date': forms.Select,
            'time': forms.Select,
        }

    def clean(self):
        cleaned_data = super().clean()
        AppointmentValidator(
            cleaned_data, self.fields, ErrorClass=ValidationError
        )
        return cleaned_data
