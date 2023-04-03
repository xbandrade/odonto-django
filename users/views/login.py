from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from users.forms import LoginForm


class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('users:dashboard'))
        form = LoginForm()
        context = {
            'form': form,
            'form_action': reverse('users:login_create'),
        }
        return render(request, 'users/pages/login.html', context=context)


class UserLoginCreateView(View):
    def get(self, request):
        raise Http404()

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            authenticated_user = authenticate(
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', ''),
            )
            if authenticated_user:
                messages.success(request, _('You are logged in'))
                login(request, authenticated_user)
            else:
                messages.error(request, _('Invalid credentials'))
        else:
            messages.error(request, _('Invalid username or password'))
        return redirect(reverse('users:dashboard'))
