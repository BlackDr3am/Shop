from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    direccion = models.TextField()  
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )
