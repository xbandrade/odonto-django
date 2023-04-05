# Generated by Django 4.1.7 on 2023-04-05 22:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0002_appointment_confirmation_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procedure', models.CharField(max_length=50, verbose_name='Procedure')),
                ('date', models.CharField(max_length=20, verbose_name='Date')),
                ('time', models.CharField(max_length=20, verbose_name='Time')),
                ('details', models.TextField(verbose_name='Details')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='Sent at')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Is confirmed')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Custom Appointment',
                'verbose_name_plural': 'Custom Appointments',
            },
        ),
    ]
