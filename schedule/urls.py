from django.urls import path

from schedule import views

app_name = 'schedule'

urlpatterns = [
    path('', views.ScheduleView.as_view(), name='schedule'),
    path('app_dates/',
         views.AvailableAppointmentDates.as_view(),
         name='dates'),
    path('app_times/',
         views.AvailableAppointmentTimes.as_view(),
         name='times'),
]
