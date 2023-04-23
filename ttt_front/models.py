from django.db import models
from tinymce import models as tinymce_models
from django_resized import ResizedImageField
from django.apps import apps # avoid circular import

class Cassette(models.Model):
    id_cassette = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    longueur = models.CharField(max_length=10, blank=True, null=True)
    description = tinymce_models.HTMLField(blank=True, null=True)
    lien_bandcamp = models.CharField(max_length=255, blank=True, null=True)
    lien_soundcloud = models.CharField(max_length=255, blank=True, null=True)
    lien_youtube = models.CharField(max_length=255, blank=True, null=True)
    date_sortie = models.DateField(blank=True, null=True)
    image_pochette = ResizedImageField(size=[600, 600], upload_to='image_cassette', blank=True, null=True)
    download = models.FileField(upload_to='file_cassette', blank=True, null=True)
    nombre_de_download = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, default=6.00)
    sold_out = models.BooleanField(default=False)
    suppr = models.BooleanField(default=False)
    publier = models.BooleanField(default=False)
    nombre_exemplaire = models.IntegerField(blank=True, null=True, default=75)

    class Meta:
        db_table = 'cassette'

    def save(self, *args, **kwargs): # surcharge save method of the models.Model
        super().save(*args, **kwargs)
        exemplaire_class = apps.get_model('ttt_back.Exemplaire') # apps.get_model avoid circular import
        if not exemplaire_class.objects.filter(id_cassette=self.id_cassette).exists(): # verify if the exemplaires for this cassette already exist, if not create all exemplaires
            for i in range(self.nombre_exemplaire):
                if 0 <= i <= 9: # first ten exemplaires are for the artist
                    id_etat = 5 # (5 == offert)
                    localisation = "Chez l'artiste"
                    commentaire = "exemplaire offert à l'artiste"
                else:
                    id_etat = 1 # (1 == en stock)
                    localisation = ""
                    commentaire = ""
                exemplaire = exemplaire_class(
                    None, # id auto increment 
                    i + 1, # numero_exemplaire
                    id_etat, # id_etat (1 == en stock)
                    localisation, # localite_exemplaire
                    None, # id_vendeur
                    0.00, # prix_vente_euros
                    False, # vente_remboursee
                    None, # id_client
                    None, # date_vente
                    0.00, # montant_frais_de_port
                    False, # frais_de_port_rembourses
                    commentaire, # commentaire
                    self.id_cassette # id_cassette
                )
                exemplaire.save()
    
    def __str__(self):
        return f"{self.code} {self.titre}"

class Artiste(models.Model):
    id_artiste = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    image_artiste = ResizedImageField(size=[600, 600], upload_to='image_artiste', blank=True, null=True)
    bio = tinymce_models.HTMLField(blank=True, null=True)
    lien_artiste = models.CharField(max_length=255, blank=True, null=True)
    suppr = models.BooleanField(default=False)

    cassette = models.ManyToManyField(Cassette, verbose_name="a produit") # , related_name="production")

    class Meta:
        db_table = 'artiste'
    
    def __str__(self):
        return self.nom

class Event(models.Model):
    id_event = models.AutoField(primary_key=True)
    date_event = models.DateField(blank=True, null=True)
    lieu = models.CharField(max_length=255, blank=True, null=True)
    titre_event = models.CharField(max_length=255, blank=True, null=True)
    description_event = tinymce_models.HTMLField(blank=True, null=True)
    image_event = ResizedImageField(size=[600, 600], upload_to='image_event', blank=True, null=True)
    suppr = models.BooleanField(default=False)

    class Meta:
        db_table = 'event'

    def __str__(self):
        return f"{self.date_event} {self.titre_event}"

class FraisDePort(models.Model):
    id_frais_de_port = models.AutoField(primary_key=True)
    nom_destination = models.CharField(max_length=25, blank=True, null=True)
    montant_frais_de_port = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'frais_de_port'
    
    def __str__(self):
        return self.nom_destination