from django import forms

from schedule.models import CustomSchedule


class CustomScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomSchedule
        fields = ('procedure', 'date', 'time', 'details')
        widgets = {
            'procedure': forms.TextInput,
            'date': forms.TextInput,
            'time': forms.TextInput,
            'details': forms.Textarea,
        }
        required = {
            'procedure': True,
            'date': True,
            'time': True,
            'details': True,
        }
