from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['cpf', 'phone_number']


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'profile']
