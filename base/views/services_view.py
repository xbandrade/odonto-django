from django.shortcuts import render

from schedule.models import Procedure

from .base_view import BaseView


class ServicesView(BaseView):
    template_name = 'global/pages/services.html'

    def get(self, request):
        procedures = Procedure.objects.all()
        context = self.get_context_data()
        context['procedures'] = procedures
        return render(request, 'global/pages/services.html', context=context)
