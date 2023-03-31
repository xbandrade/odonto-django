from django.shortcuts import render
from django.views import View


class BaseView(View):
    template_name = ''

    def get(self, request):
        curr_path = request.path
        context = {
            'curr_path': curr_path,
        }
        return render(
            self.request,
            self.template_name,
            context
        )
