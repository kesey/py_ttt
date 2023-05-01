from django.urls import path
import ttt_front.views

urlpatterns = [
    path('label/', ttt_front.views.label, name="label"),
    path('', ttt_front.views.home, name='home'),
    path('cassette/<int:id_cassette>/', ttt_front.views.cassette_detail, name="cassette_detail"),
    path('cassette/<int:id_cassette>/download/', ttt_front.views.download, name="download"),
    path('artistes/', ttt_front.views.artistes, name="artistes"),
    path('artiste/<int:id_artiste>/', ttt_front.views.artiste_detail, name="artiste_detail"),
    path('events/', ttt_front.views.events, name="events"),
    path('event/<int:id_event>/', ttt_front.views.event_detail, name="event_detail"),
    path('live_archives/', ttt_front.views.live_archives, name="live_archives"),
    path('links/', ttt_front.views.links, name="links"),
    path('contact/', ttt_front.views.contact, name="contact")
]