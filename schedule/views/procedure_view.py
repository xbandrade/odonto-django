from django.http import JsonResponse
from django.views import View

from schedule.models import Procedure


class ProcedurePrice(View):
    def get(self, request, id):
        procedure = Procedure.objects.get(id=id)
        price = procedure.price
        return JsonResponse({'price': price})
