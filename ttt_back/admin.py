from django.contrib import admin
from ttt_back.models import Client, Exemplaire, EtatExemplaire

class ExemplaireAdmin(admin.ModelAdmin):
    list_display = ("numero_exemplaire", "id_cassette")

admin.site.register(Client)
admin.site.register(Exemplaire, ExemplaireAdmin)
admin.site.register(EtatExemplaire)
