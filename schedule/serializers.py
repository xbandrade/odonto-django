from rest_framework import serializers

from schedule.models import Appointment
from schedule.validators import AppointmentValidator


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'procedure', 'scheduled_at',
            'updated_at', 'is_completed', 'is_confirmed', 'date', 'time',
            'confirmation_token',
        ]
        read_only_fields = fields

    procedure = serializers.StringRelatedField(read_only=True)

    def validate(self, data):
        super_validate = super().validate(data)
        AppointmentValidator(
            data=data,
            ErrorClass=serializers.ValidationError,
        )
        return super_validate
