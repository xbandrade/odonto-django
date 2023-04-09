import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Procedure(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    name_pt = models.CharField(max_length=100, verbose_name=_('PT Name'))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Price'),
    )

    class Meta:
        verbose_name = _('Procedure')
        verbose_name_plural = _('Procedures')

    def __str__(self) -> str:
        return f'#{self.id} - {self.name}'


class AppointmentManager(models.Manager):
    def get_open_appointments(self):
        return self.filter(
            is_completed=False,
        ).order_by('-id').select_related('procedure', 'user')


class Appointment(models.Model):
    objects = AppointmentManager()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True,
        verbose_name=_('User'),
    )
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Scheduled at')
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated at')
    )
    is_completed = models.BooleanField(
        default=False, verbose_name=_('Is completed')
    )
    is_confirmed = models.BooleanField(
        default=False, verbose_name=_('Is confirmed')
    )
    date = models.DateField(verbose_name=_('Date'))
    time = models.TimeField(verbose_name=_('Time'))
    confirmation_token = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True,
        verbose_name=_('Confirmation token')
    )

    class Meta:
        unique_together = ('date', 'time')
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')

    def __str__(self):
        name = self.user.first_name if self.user else 'NONE'
        return _("#{id} - {name}'s Appointment").format(
            id=self.id,
            name=name,
        )


class CustomSchedule(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True,
        verbose_name=_('User'),
    )
    procedure = models.CharField(max_length=50, verbose_name=_('Procedure'))
    date = models.CharField(max_length=20, verbose_name=_('Date'))
    time = models.CharField(max_length=20, verbose_name=_('Time'))
    details = models.TextField(verbose_name=_('Details'))
    sent_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Sent at')
    )
    is_confirmed = models.BooleanField(
        default=False, verbose_name=_('Is confirmed')
    )

    class Meta:
        verbose_name = _('Custom Appointment')
        verbose_name_plural = _('Custom Appointments')

    def __str__(self):
        name = self.user.first_name if self.user else 'NONE'
        return _("#{id} - {name}'s Custom Appointment").format(
            id=self.id,
            name=name,
        )
