from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ProfileForm(forms.ModelForm):
    cpf = forms.CharField(max_length=14, required=False)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Profile
        fields = ('cpf', 'phone_number')


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email',
                    'full_name', 'cpf', 'phone_number')
    form = ProfileForm
    inlines = (ProfileInline,)

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def cpf(self, obj):
        return obj.profile.cpf

    def phone_number(self, obj):
        return obj.profile.phone_number

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
        profile, _ = Profile.objects.get_or_create(user=obj)
        profile.cpf = form.cleaned_data['cpf']
        profile.phone_number = form.cleaned_data['phone_number']
        profile.save()

    full_name.short_description = _('Name')
    cpf.short_description = _('CPF')
    phone_number.short_description = _('Phone number')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
