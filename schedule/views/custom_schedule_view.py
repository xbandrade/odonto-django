from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from schedule.forms import CustomScheduleForm


class CustomScheduleView(View):
    template_name = 'schedule/pages/custom_schedule.html'

    def get(self, request):
        form = CustomScheduleForm()
        curr_path = request.path
        context = {
            'curr_path': curr_path,
            'form': form,
        }
        return render(
            self.request,
            self.template_name,
            context
        )

    def post(self, request):
        form = CustomScheduleForm(request.POST or None)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.is_confirmed = False
            appointment.is_completed = False
            appointment.save()
            messages.success(
                request,
                _('Thank you for submitting your custom treatment request! '
                  'Our team will promptly review your request and '
                  'provide a response via email.')
            )
            return redirect(reverse('users:dashboard'))
        messages.error(request, _('Failed to book your custom appointment!'))
        context = {
            'schedule_failed': True,
        }
        return render(self.request, self.template_name, context=context)
