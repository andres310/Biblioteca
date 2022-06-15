from django.db import models
from django.contrib.auth.models import AbstractUser

# Sustituye el usuario por defecto por uno con medidas más seguras
class CustomUser(AbstractUser):
    def __str__(self) -> str:
        return self.username