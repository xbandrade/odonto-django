from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from users import views

app_name = 'users'
user_api_router = SimpleRouter()
user_api_router.register(
    'api',
    views.UserAPIViewSet,
    basename='user-api',
)

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('login_create/', views.UserLoginCreateView.as_view(),
         name='login_create'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('clear/', views.ClearSessionView.as_view(), name='clear'),
    path('delete/', views.DashboardAppointmentDelete.as_view(),
         name='appointment_delete'),
    path('api/token/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/',
         TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += user_api_router.urls
