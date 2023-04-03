from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Appointment, Procedure


class ProcedureAdmin(admin.ModelAdmin):
    ...


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'procedure', 'date', 'time',
                    'price', 'is_confirmed', 'is_completed')
    list_display_links = 'id', 'date', 'time'
    search_fields = 'id', 'user', 'procedure', 'scheduled_at', 'updated_at'
    list_filter = 'procedure', 'is_confirmed', 'is_completed'
    list_per_page = 10
    list_editable = 'is_confirmed', 'is_completed'
    ordering = '-id',

    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def price(self, obj):
        return obj.procedure.price

    full_name.short_description = _('Name')
    price.short_description = _('Price')


admin.site.register(Procedure, ProcedureAdmin)
