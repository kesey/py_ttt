# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    identifiant = models.CharField(max_length=255, blank=True, null=True)
    mot_de_passe = models.CharField(max_length=255, blank=True, null=True)
    suppr = models.IntegerField()
    a_rembourse = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    a_recupere = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Artiste(models.Model):
    id_artiste = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    image_artiste = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    lien_artiste = models.CharField(max_length=255, blank=True, null=True)
    suppr = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'artiste'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthenticationUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'authentication_user'


class AuthenticationUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'authentication_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthenticationUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'authentication_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Cassette(models.Model):
    id_cassette = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    longueur = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lien_bandcamp = models.CharField(max_length=255, blank=True, null=True)
    lien_soundcloud = models.CharField(max_length=255, blank=True, null=True)
    lien_youtube = models.CharField(max_length=255, blank=True, null=True)
    date_sortie = models.DateField(blank=True, null=True)
    image_pochette = models.CharField(max_length=50, blank=True, null=True)
    download = models.CharField(max_length=50, blank=True, null=True)
    nombre_de_download = models.IntegerField()
    prix = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    sold_out = models.IntegerField()
    suppr = models.IntegerField()
    publier = models.IntegerField(blank=True, null=True)
    nombre_exemplaire = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cassette'


class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    adresse_client = models.CharField(max_length=255, blank=True, null=True)
    mail_client = models.CharField(max_length=50, blank=True, null=True)
    nom_client = models.CharField(max_length=50, blank=True, null=True)
    suppr = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'client'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EtatExemplaire(models.Model):
    id_etat_exemplaire = models.AutoField(primary_key=True)
    description_etat = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'etat_exemplaire'


class Event(models.Model):
    id_event = models.AutoField(primary_key=True)
    date_event = models.DateField(blank=True, null=True)
    lieu = models.CharField(max_length=255, blank=True, null=True)
    titre_event = models.CharField(max_length=255, blank=True, null=True)
    description_event = models.TextField(blank=True, null=True)
    image_event = models.CharField(max_length=255, blank=True, null=True)
    suppr = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'event'


class Exemplaire(models.Model):
    id_exemplaire = models.AutoField(primary_key=True)
    numero_exemplaire = models.IntegerField(blank=True, null=True)
    prix_vente_euros = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    vente_remboursee = models.IntegerField()
    date_vente = models.DateField(blank=True, null=True)
    localite_exemplaire = models.CharField(max_length=150, blank=True, null=True)
    commentaire = models.CharField(max_length=255, blank=True, null=True)
    montant_frais_de_port = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    frais_de_port_rembourses = models.IntegerField()
    id_vendeur = models.IntegerField(blank=True, null=True)
    id_cassette = models.ForeignKey(Cassette, models.DO_NOTHING, db_column='id_cassette')
    id_etat = models.ForeignKey(EtatExemplaire, models.DO_NOTHING, db_column='id_etat')
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exemplaire'


class FraisDePort(models.Model):
    id_frais_de_port = models.AutoField(primary_key=True)
    nom_destination = models.CharField(max_length=25, blank=True, null=True)
    montant_frais_de_port = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frais_de_port'


class Produire(models.Model):
    id_cassette = models.PositiveIntegerField(primary_key=True)  # The composite primary key (id_cassette, id_artiste) found, that is not supported. The first column is selected.
    id_artiste = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'produire'
        unique_together = (('id_cassette', 'id_artiste'),)
