from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from schedule.models import Appointment, Procedure
from schedule.serializers import AppointmentSerializer, ProcedureSerializer


class ScheduleAPIViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        qs = Appointment.objects.filter(user=self.request.user).order_by('-id')
        return qs

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )
        if obj.user != self.request.user:
            raise PermissionDenied(
                'You are not allowed to access this appointment.'
            )
        return obj

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['domain'] = get_current_site(self.request)
        context['current_user'] = self.request.user
        return context

    def create(self, request, *args, **kwargs):
        serializer_data = {
            'user': request.user.id,
            'domain': get_current_site(request),
            **request.data,
        }
        serializer = AppointmentSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        logged_user = request.user
        appointment_user = serializer.validated_data.get('user')
        if logged_user.id != appointment_user.id:
            raise PermissionDenied(
                'You are not allowed to schedule for another user.'
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProcedureAPIViewSet(ModelViewSet):
    serializer_class = ProcedureSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        qs = Procedure.objects.order_by('-id')
        return qs

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )
        return obj

    def create(self, request, *args, **kwargs):
        serializer = ProcedureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logged_user = request.user
        if not logged_user.is_staff:
            raise PermissionDenied(
                'You need to be a staff member to create a new procedure'
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        logged_user = request.user
        if not logged_user.is_staff:
            raise PermissionDenied(
                'You need to be a staff member to update a procedure'
            )
        serializer = ProcedureSerializer(
            instance=obj,
            data=request.data,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
