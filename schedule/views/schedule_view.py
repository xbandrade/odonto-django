from django.shortcuts import render
from django.views import View


class ScheduleView(View):
    template_name = 'schedule/pages/schedule.html'

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
