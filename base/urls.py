from django.urls import path

from base import views

app_name = 'base'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('treatments/', views.TreatmentsView.as_view(), name='treatments'),
    path('about/', views.AboutView.as_view(), name='about'),
]
