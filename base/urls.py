from django.urls import path

from base import views

app_name = 'base'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('about/', views.AboutView.as_view(), name='about'),
]
