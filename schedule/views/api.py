from datetime import datetime, time, timedelta

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from schedule.models import Appointment, Procedure
from schedule.serializers import AppointmentSerializer, ProcedureSerializer
from utils.pagination import AppointmentPagination


class ScheduleAPIViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    pagination_class = AppointmentPagination
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = Appointment.objects.all().order_by('-id')
        else:
            qs = Appointment.objects.filter(
                user=self.request.user).order_by('-id')
        return qs

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )
        if obj.user != self.request.user and not self.request.user.is_staff:
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
        if logged_user.id != appointment_user.id and not logged_user.is_staff:
            raise PermissionDenied(
                'You are not allowed to schedule for another user.'
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserAppointmentAPIViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    pagination_class = AppointmentPagination
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', ]

    def get_queryset(self):
        if not self.request.user.is_staff:
            raise PermissionDenied(
                'You are not allowed to access these appointments.')
        user_id = self.kwargs.get('pk', 0)
        qs = Appointment.objects.filter(user__id=user_id).order_by('-id')
        return qs


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


class ExistingAppointmentsAPIViewSet(ViewSet):
    permission_classes = [IsAdminUser, ]

    def list(self, request):
        current_datetime = datetime.now()
        next_available_date = current_datetime.date() + timedelta(days=1)
        existing_appointments = Appointment.objects.filter(
            date__range=[next_available_date,
                         next_available_date + timedelta(days=14)]
        ).values('date', 'time')
        response_data = {
            'next_appointments': existing_appointments
        }
        return Response(response_data)


class AvailableDateTimeAPIViewSet(ViewSet):
    permission_classes = [IsAdminUser, ]

    def list(self, request):
        current_datetime = datetime.now()
        next_available_date = current_datetime.date() + timedelta(days=1)
        existing_appointments = Appointment.objects.filter(
            date__range=[next_available_date,
                         next_available_date + timedelta(days=14)]
        ).values('date', 'time')
        existing_dates = set(appt['date'] for appt in existing_appointments)
        existing_times = set(appt['time'] for appt in existing_appointments)
        available_datetime_strings = []
        for _ in range(15):
            while next_available_date.weekday() == 6:  # sunday
                next_available_date += timedelta(days=1)
            start_time = datetime.combine(
                next_available_date, time(hour=8)
            )
            end_time = datetime.combine(
                next_available_date, time(hour=17)
            )
            current_time = start_time
            while current_time <= end_time:
                if (
                    current_time.date() not in existing_dates
                    or current_time.time() not in existing_times
                ):
                    available_datetime_strings.append(
                        current_time.strftime('%Y-%m-%d %H:%M')
                    )
                current_time += timedelta(hours=1)
            next_available_date += timedelta(days=1)
        response_data = {
            'available_datetimes': available_datetime_strings
        }
        return Response(response_data)
