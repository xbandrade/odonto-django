from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Procedure(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    pt_name = models.CharField(max_length=100, verbose_name=_('PT Name'))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Price'),
    )

    class Meta:
        verbose_name = _('Procedure')
        verbose_name_plural = _('Procedures')

    def __str__(self) -> str:
        return f'{self.name} - R${self.price}'


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
