from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .base_view import BaseView


class AboutView(BaseView):
    template_name = 'global/pages/about.html'

    def get(self, request):
        context = self.get_context_data()
        about_text = [
            _("We are a premier dental clinic dedicated "
              "to providing the highest quality dental care to "
              "our patients."),
            _("At OdontoDj, we offer a full range of dental services, "
              "from routine check-ups and cleanings to complex restorative "
              "procedures. Our facility is equipped with the "
              "latest technology and equipment to ensure that you receive the "
              "best possible care."),
            _("In addition to our exceptional dental services, we are proud "
              "to offer convenient online appointment scheduling and access "
              "to your treatment history. This means that you can easily "
              "schedule your next appointment from the comfort of your own "
              "home, and keep track of your previous treatments "
              "and progress."),
            _("Thank you for choosing OdontoDj for your dental "
              "needs. We look forward to helping you achieve a healthy, "
              "beautiful smile!"),
        ]
        context['about_text'] = about_text
        return render(
            self.request,
            self.template_name,
            context
        )
