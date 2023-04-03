from django.shortcuts import render
from django.views import View


class BaseView(View):
    template_name = ''

    def get_context_data(self):
        curr_path = self.request.path
        context = {
            'curr_path': curr_path,
        }
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(
            self.request,
            self.template_name,
            context
        )
