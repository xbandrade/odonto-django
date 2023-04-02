from django.contrib import admin

from users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...
