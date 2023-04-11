from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from users.forms import ChangePasswordForm, UpdateForm


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class UserUpdateView(View):
    template_name = 'users/pages/update.html'

    def get(self, request):
        form = UpdateForm(instance=request.user)
        context = {
            'form': form,
            'form_action': reverse('users:update'),
            'update': True,
        }
        return render(request, self.template_name, context=context)

    def get_updated_data(self, user, data):
        for key in data:
            if isinstance(data[key], list):
                data[key] = data[key][0]
        profile = data.get('profile', {})
        phone_number = profile.get('phone_number', user.profile.phone_number)
        return {
            'username': data.get('username', user.username),
            'password': data.get('password', user.password),
            'password2': data.get('password2', user.password),
            'email': data.get('email', user.email),
            'first_name': data.get('first_name', user.first_name),
            'last_name': data.get('last_name', user.last_name),
            'cpf': user.profile.cpf,
            'phone_number': phone_number,
        }

    def post(self, request):
        POST = request.POST
        form_data = self.get_updated_data(request.user, POST)
        form = UpdateForm(form_data, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            request.user.profile.phone_number = form.cleaned_data.get(
                'phone_number', '')
            request.user.profile.save()
            user.save()
            user_updated = _('User information has been updated')
            messages.success(request, user_updated)
            return redirect(reverse('users:dashboard'))
        context = {
            'form': form,
            'form_action': reverse('users:update'),
        }
        return render(request, self.template_name, context=context)


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class PasswordUpdateView(View):
    template_name = 'users/pages/change_password.html'

    def get(self, request):
        form = ChangePasswordForm()
        context = {
            'form': form,
            'form_action': reverse('users:change_password'),
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        POST = request.POST
        form = ChangePasswordForm(POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data.get('password'))
            request.user.save()
            user_updated = _('Password has been changed successfully')
            messages.success(request, user_updated)
            return redirect(reverse('users:dashboard'))
        context = {
            'form': form,
            'form_action': reverse('users:change_password'),
        }
        return render(request, self.template_name, context=context)
