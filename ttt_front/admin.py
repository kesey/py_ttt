from django.contrib import admin
from ttt_front.models import Cassette, Artiste, Event, FraisDePort

class EventAdmin(admin.ModelAdmin):
    list_display = ("date_event", "titre_event")

admin.site.register(Event, EventAdmin)

class CassetteAdmin(admin.ModelAdmin):
    list_display = ("code", "titre")

admin.site.register(Cassette, CassetteAdmin)

models = (Artiste, FraisDePort)
admin.site.register(models)
