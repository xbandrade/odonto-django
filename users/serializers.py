from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.forms import RegisterForm, UpdateForm
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
    is_staff = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'password2', 'cpf',
                  'phone_number', 'is_staff']

    def get_is_staff(self, user):
        return user.is_staff

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

    def get_updated_data(self, user, validated_data):
        profile = validated_data.get('profile', {})
        phone_number = profile.get('phone_number', user.profile.phone_number)
        return {
            'username': validated_data.get('username', user.username),
            'password': validated_data.get('password', user.password),
            'password2': validated_data.get('password2', user.password),
            'email': validated_data.get('email', user.email),
            'first_name': validated_data.get('first_name', user.first_name),
            'last_name': validated_data.get('last_name', user.last_name),
            'cpf': user.profile.cpf,
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

    def update(self, user, validated_data):
        form_data = self.get_updated_data(user, validated_data)
        update_form = UpdateForm(data=form_data, instance=user)
        if update_form.is_valid():
            user.username = form_data.get(
                'username', user.username)
            user.first_name = form_data.get(
                'first_name', user.first_name)
            user.last_name = form_data.get(
                'last_name', user.last_name)
            user.email = form_data.get('email', user.email)
            user.profile.phone_number = form_data.get(
                'phone_number', user.profile.phone_number)
            user.save()
            return user
        else:
            raise serializers.ValidationError(update_form.errors)

    def validate(self, data):
        if self.context['request'].method != 'PATCH':
            if not data.get('profile'):
                raise serializers.ValidationError(
                    'Profile data cannot be empty.')
            if data['password'] != data['password2']:
                raise serializers.ValidationError('Passwords must match.')
        return data
