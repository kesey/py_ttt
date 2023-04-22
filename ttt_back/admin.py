from django.contrib import admin
from ttt_back.models import Client, ComptaVendeur
from ttt_back.views import gestion_exemplaire, compta
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.autodiscover()

admin.site.register_view(
    'gestion_exemplaire/', 
    name="gestion des exemplaires", # name is the link to display in admin interface
    view=gestion_exemplaire, 
    urlname="gestion_exemplaire", # urlname is a shortcut to target the view in templates for example
    visible=True
)

admin.site.register_view('compta/', name="comptabilité", view=compta, urlname="compta")

class ComptaVendeurAdmin(admin.ModelAdmin):
    list_display = ("id_vendeur", "a_rembourse", "a_recupere")
    # readonly_fields=('id_vendeur',)

admin.site.register(ComptaVendeur, ComptaVendeurAdmin)

admin.site.register(Client)
