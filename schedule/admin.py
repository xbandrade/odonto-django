from django.contrib import admin

from .models import Appointment, Procedure


class ProcedureAdmin(admin.ModelAdmin):
    ...


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'procedure', 'date', 'time',
                    'is_confirmed', 'is_completed')
    list_display_links = 'user', 'date', 'time'
    search_fields = 'id', 'user', 'procedure', 'scheduled_at', 'updated_at'
    list_filter = 'procedure', 'user', 'is_confirmed', 'is_completed'
    list_per_page = 10
    list_editable = 'is_confirmed', 'is_completed'
    ordering = '-id',


admin.site.register(Procedure, ProcedureAdmin)
