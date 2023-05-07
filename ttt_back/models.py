from django.db import models
from ttt_front.models import Cassette
from django.conf import settings

class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    adresse_client = models.CharField(max_length=255, blank=True, null=True)
    mail_client = models.CharField(max_length=50, blank=True, null=True)
    nom_client = models.CharField(max_length=50, blank=True, null=True)
    suppr = models.BooleanField(default=False)

    class Meta:
        db_table = 'client'
    
    def __str__(self):
        return f"{self.nom_client}"
    
class EtatExemplaire(models.Model):
    id_etat_exemplaire = models.AutoField(primary_key=True)
    description_etat = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'etat_exemplaire'
    
    def __str__(self):
        return self.description_etat

class Exemplaire(models.Model):
    id_exemplaire = models.AutoField(primary_key=True)
    numero_exemplaire = models.IntegerField(blank=True, null=True)
    id_etat_exemplaire = models.ForeignKey(EtatExemplaire, models.DO_NOTHING, blank=True, null=True)
    localite_exemplaire = models.CharField(max_length=150, blank=True, null=True)
    id_vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    prix_vente_euros = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    vente_remboursee = models.BooleanField(default=False)
    id_client = models.ForeignKey(Client, models.DO_NOTHING, blank=True, null=True)
    date_vente = models.DateField(blank=True, null=True)
    montant_frais_de_port = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    frais_de_port_rembourses = models.BooleanField(default=False)
    commentaire = models.CharField(max_length=255, blank=True, null=True)
    id_cassette = models.ForeignKey(Cassette, models.CASCADE, blank=True, null=True)
    
    class Meta:
        db_table = 'exemplaire'

    def __str__(self):
        return f"{self.numero_exemplaire} {self.id_cassette}"
    
class ComptaVendeur(models.Model):
    id_compta_vendeur = models.AutoField(primary_key=True)
    id_vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True) # , editable=False)
    a_rembourse = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0)
    a_recupere = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, default=0)

    class Meta:
        db_table = 'compta_vendeur'
    
    def __str__(self):
        return f"{self.id_vendeur}"


