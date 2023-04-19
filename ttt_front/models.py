from django.db import models
from tinymce import models as tinymce_models
from django_resized import ResizedImageField

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
    # image_pochette = models.ImageField(verbose_name="image de la pochette", null=True)
    image_pochette = ResizedImageField(size=[600, 600], upload_to='image_cassette', blank=True, null=True)
    download = models.FileField(upload_to='file_cassette', blank=True, null=True)
    nombre_de_download = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    sold_out = models.BooleanField(default=False)
    suppr = models.BooleanField(default=False)
    publier = models.BooleanField(default=False)
    nombre_exemplaire = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'cassette'
    
    def __str__(self):
        return f"{self.code} {self.titre}"

class Artiste(models.Model):
    id_artiste = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    # image_artiste = models.ImageField(verbose_name="image de l'artiste", null=True)
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
    # image_event = models.ImageField(verbose_name="image de l'event", null=True)
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