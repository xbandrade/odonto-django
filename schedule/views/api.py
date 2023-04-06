from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from schedule.models import Appointment
from schedule.serializers import AppointmentSerializer


class UserAPIViewSet(ReadOnlyModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = Appointment.objects.filter(user=self.request.user)
        return qs
