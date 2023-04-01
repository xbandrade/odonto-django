from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('login_create/', views.UserLoginCreateView.as_view(),
         name='login_create'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('clear/', views.ClearSessionView.as_view(), name='clear'),
]
