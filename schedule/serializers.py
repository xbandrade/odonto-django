from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from schedule.forms.appointment_form import AppointmentForm
from schedule.forms.procedure_form import ProcedureForm
from schedule.models import Appointment, Procedure


class AppointmentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    confirmation_link = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    procedure = serializers.CharField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'user_full_name', 'procedure', 'scheduled_at',
            'updated_at', 'is_completed', 'is_confirmed', 'date', 'time',
            'confirmation_token', 'confirmation_link', 'price'
        ]
        read_only_fields = ['confirmation_link', 'price']

    def get_price(self, obj):
        return obj.procedure.price

    def get_confirmation_link(self, obj):
        site_url = self.context.get(
            'domain') or self.initial_data.get('domain')
        if not site_url:
            return None
        return f'http://{site_url}/schedule/confirm/{obj.confirmation_token}/'

    def get_user_full_name(self, obj):
        if obj.user:
            return f'{obj.user.first_name} {obj.user.last_name}'
        return 'NONE'

    def to_internal_value(self, data):
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]
        procedure_data = data.get('procedure')
        try:
            procedure_data = int(procedure_data)
            procedure = Procedure.objects.filter(id=procedure_data).first()
        except (TypeError, ValueError):
            procedure = Procedure.objects.filter(
                Q(name=procedure_data) | Q(name_pt=procedure_data)).first()
        if not procedure_data:
            raise serializers.ValidationError(
                {'procedure': _('This field is required.')})
        if not procedure:
            raise serializers.ValidationError(
                {'procedure': _('Invalid procedure selected.')})
        data['procedure'] = procedure.name
        return super().to_internal_value(data)

    def get_form_data(self, validated_data):
        name = validated_data.get('procedure')
        procedure = Procedure.objects.filter(name=name).first()
        return {
            'user': validated_data.get('user'),
            'domain': validated_data.get('domain'),
            'date': validated_data.get('date'),
            'time': validated_data.get('time'),
            'procedure': procedure,
        }

    def create(self, validated_data):
        form_data = self.get_form_data(validated_data)
        appointment_form = AppointmentForm(form_data)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.user = form_data.get('user')
            appointment.procedure = form_data['procedure']
            appointment.save()
            return appointment
        else:
            raise serializers.ValidationError(appointment_form.errors)

    def validate(self, data):
        super_validate = super().validate(data)
        return super_validate


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = [
            'id', 'name', 'name_pt', 'price', 'description', 'description_pt'
        ]

    def get_form_data(self, validated_data):
        return {
            'name': validated_data.get('name'),
            'name_pt': validated_data.get('name_pt'),
            'price': validated_data.get('price'),
            'description': validated_data.get('description'),
            'description_pt': validated_data.get('description_pt'),
        }

    def create(self, validated_data):
        form_data = self.get_form_data(validated_data)
        procedure_form = ProcedureForm(form_data)
        if procedure_form.is_valid():
            procedure = procedure_form.save()
            return procedure
        else:
            raise serializers.ValidationError(procedure_form.errors)

    def validate(self, data):
        super_validate = super().validate(data)
        return super_validate
