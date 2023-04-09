from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.forms import RegisterForm
from users.models import Profile


class UserSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(source='profile.cpf')
    phone_number = serializers.CharField(
        source='profile.phone_number', required=False)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'password2', 'cpf', 'phone_number']

    def get_form_data(self, validated_data):
        profile = validated_data.get('profile')
        cpf = profile.get('cpf', '')
        phone_number = profile.get('phone_number', '')
        return {
            'username': validated_data.get('username', ''),
            'password': validated_data.get('password', ''),
            'password2': validated_data.get('password2', ''),
            'email': validated_data.get('email', ''),
            'first_name': validated_data.get('first_name', ''),
            'last_name': validated_data.get('last_name', ''),
            'cpf': cpf,
            'phone_number': phone_number,
        }

    def create(self, validated_data):
        form_data = self.get_form_data(validated_data)
        register_form = RegisterForm(form_data)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(validated_data['password'])
            user.save()
            profile = Profile.objects.create(
                user=user,
                cpf=form_data['cpf'],
                phone_number=form_data.get('phone_number', ''),
            )
            profile.save()
            return user
        else:
            raise serializers.ValidationError(register_form.errors)

    def validate(self, data):
        if not data.get('profile'):
            raise serializers.ValidationError('Profile data cannot be empty.')
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data
