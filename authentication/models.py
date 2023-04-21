from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    a_rembourse = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0)
    a_recupere = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0)
    suppr = models.BooleanField(default=False)
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return self.username