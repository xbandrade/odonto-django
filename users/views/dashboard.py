from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class UserDashboardView(LoginRequiredMixin, View):
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'users/pages/dashboard.html')
