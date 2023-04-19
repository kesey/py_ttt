from django.contrib import admin
from ttt_back.models import Client # , Exemplaire
from ttt_back.views import gestion_exemplaire, Compta
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

admin.site.register_view('compta/', name="comptabilité", view=Compta.as_view(), urlname="compta")

admin.site.register(Client)
