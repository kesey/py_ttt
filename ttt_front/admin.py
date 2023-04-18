from django.contrib import admin
from ttt_front.models import Cassette, Artiste, Event, FraisDePort

class EventAdmin(admin.ModelAdmin):
    list_display = ("date_event", "titre_event")

class CassetteAdmin(admin.ModelAdmin):
    list_display = ("code", "titre")

admin.site.register(Cassette, CassetteAdmin)
admin.site.register(Artiste)
admin.site.register(Event, EventAdmin)
admin.site.register(FraisDePort)
