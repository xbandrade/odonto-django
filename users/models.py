from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=20)
