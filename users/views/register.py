from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from users.forms import RegisterForm


class UserRegisterView(View):
    def get(self, request):
        register_form_data = request.session.get('register_form_data')
        form = RegisterForm(register_form_data)
        context = {
            'form': form,
            'form_action': reverse('users:create'),
        }
        return render(
            request, 'users/pages/register.html', context=context
        )


class UserCreateView(View):
    def get(self, request):
        raise Http404()

    def post(self, request):
        POST = request.POST
        request.session['register_form_data'] = POST
        form = RegisterForm(POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            user_created_translation = _(
                'User has been created, please log in'
            )
            messages.success(request, user_created_translation)
            del request.session['register_form_data']
            return redirect(reverse('users:login'))
        return redirect('users:register')


class ClearSessionView(View):
    http_method_names = ['post']

    def get(self, request):
        raise Http404()

    def post(self, request):
        if 'register_form_data' in request.session:
            del request.session['register_form_data']
        return JsonResponse({'success': True})
