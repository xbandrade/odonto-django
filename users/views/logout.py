from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View


class UserLogoutView(LoginRequiredMixin, View):
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get(self, request):
        messages.error(request, _('Invalid logout request'))
        return redirect(reverse('users:login'))

    def post(self, request):
        if request.POST.get('username') != request.user.username:
            messages.error(request, _('Invalid logout user'))
        else:
            logout(request)
            messages.success(request, _('Logged out successfully'))
        return redirect(reverse('users:login'))
