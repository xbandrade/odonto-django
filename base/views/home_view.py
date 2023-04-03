from django.shortcuts import render

from .base_view import BaseView


class HomeView(BaseView):
    template_name = 'global/pages/home.html'

    def get(self, request):
        context = self.get_context_data()
        context['is_home'] = True
        return render(
            self.request,
            self.template_name,
            context
        )
