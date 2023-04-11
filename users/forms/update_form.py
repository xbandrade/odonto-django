from string import ascii_letters as letters

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.forms import RegisterForm
from users.models import User


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput, label=_('New Password'))
    password2 = forms.CharField(
        widget=forms.PasswordInput, label=_('Confirm New Password'))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError(
                _('Passwords must match'), code='invalid')


class UpdateForm(RegisterForm):
    password_form = ChangePasswordForm()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'cpf',
            'phone_number',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile = self.instance.profile
        del self.fields['password']
        del self.fields['password2']
        self.fields['cpf'].disabled = True
        self.fields['cpf'].widget.attrs['readonly'] = True
        self.fields['cpf'].initial = profile.cpf
        self.fields['cpf'].help_text = ''
        self.fields['phone_number'].initial = profile.phone_number

    def clean_cpf(self):
        return self.instance.profile.cpf

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '')
        if phone_number == self.instance.profile.phone_number:
            return phone_number
        if any(char in phone_number for char in letters):
            raise ValidationError(
                _('The phone number provided is invalid'), code='invalid'
            )
        self.instance.profile.phone_number = phone_number
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email == self.instance.email:
            return email
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                _('User email is already in use'), code='unique'
            )
        return email
