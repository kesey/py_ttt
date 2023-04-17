from django.db import models
from django.contrib.auth.models import AbstractUser

# class Admin(models.Model): # from python manage.py inspectdb
#     id_admin = models.AutoField(primary_key=True)
#     nom = models.CharField(max_length=255, blank=True, null=True)
#     identifiant = models.CharField(max_length=255, blank=True, null=True)
#     mot_de_passe = models.CharField(max_length=255, blank=True, null=True)
#     suppr = models.IntegerField()
#     a_rembourse = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
#     a_recupere = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

#     class Meta:
#         db_table = 'admin'

class User(AbstractUser):
    a_rembourse = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    a_recupere = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.username