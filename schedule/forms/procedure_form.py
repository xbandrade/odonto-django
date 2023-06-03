from django import forms

from schedule.models import Procedure


class ProcedureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Procedure
        fields = ('name', 'name_pt', 'price', 'description', 'description_pt')
        widgets = {
            'name': forms.TextInput,
            'name_pt': forms.TextInput,
            'price': forms.TextInput,
            'description': forms.Textarea,
            'description_pt': forms.Textarea,
        }
        required = {
            'name': True,
            'name_pt': True,
            'price': True,
            'description': True,
            'description_pt': True,
        }
