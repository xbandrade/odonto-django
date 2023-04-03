from django.views import View


class BaseView(View):
    template_name = ''

    def get_context_data(self):
        curr_path = self.request.path
        context = {
            'curr_path': curr_path,
        }
        return context
