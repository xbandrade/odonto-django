from django.urls import path
from rest_framework.routers import SimpleRouter

from schedule import views

app_name = 'schedule'
schedule_api_router = SimpleRouter()
schedule_api_router.register(
    'api',
    views.ScheduleAPIViewSet,
    basename='schedule-api',
)
procedure_api_router = SimpleRouter()
procedure_api_router.register(
    r'api/procedure',
    views.ProcedureAPIViewSet,
    basename='procedure-api',
)

urlpatterns = [
    path('', views.ScheduleView.as_view(), name='schedule'),
    path('app_dates/',
         views.AvailableAppointmentDates.as_view(),
         name='dates'),
    path('app_times/',
         views.AvailableAppointmentTimes.as_view(),
         name='times'),
    path('get_price/<int:id>/',
         views.ProcedurePrice.as_view(),
         name='price'),
    path('confirm/<str:token>/',
         views.AppointmentConfirmationView.as_view(),
         name='confirm'),
    path('custom/',
         views.CustomScheduleView.as_view(),
         name='custom'),
]

urlpatterns += procedure_api_router.urls
urlpatterns += schedule_api_router.urls
