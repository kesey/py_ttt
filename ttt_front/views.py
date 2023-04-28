from django.shortcuts import render
from ttt_front.models import Cassette, Artiste, Event, FraisDePort
from django.core.paginator import Paginator

def label(request):
    return render(
        request,
        "ttt_front/label.html"
    )

def home(request):
    cassettes = Cassette.objects.all().order_by("-date_sortie")
    paginator = Paginator(cassettes, 20)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    artistes = {}
    for cassette in page: # get artistes for each cassette
        artistes[cassette.id_cassette] = Artiste.objects.filter(cassette=cassette)
    context = { 
        "page": page,
        "artistes": artistes
    }
    return render(
        request,
        "ttt_front/home.html",
        context=context
    )

def cassette_detail(request, id_cassette):
    cassette = Cassette.objects.filter(id_cassette=id_cassette)
    artistes = cassette.get().artiste_set.all()
    frais_de_port = FraisDePort.objects.all()
    context = { 
        "cassette": cassette,
        "artistes": artistes,
        "frais_de_port": frais_de_port,
    }
    return render(
        request,
        "ttt_front/cassette_detail.html",
        context=context
    )

def artistes(request):
    artistes = Artiste.objects.all().order_by("-id_artiste")
    paginator = Paginator(artistes, 20)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = { 
        "page": page
    }
    return render(
        request,
        "ttt_front/artiste.html",
        context=context
    )

def artiste_detail(request, id_artiste):
    artiste = Artiste.objects.filter(id_artiste=id_artiste)
    cassettes = artiste.get().cassette.all()
    artistes = {}
    for cassette in cassettes: # get artistes for each cassette
        artistes[cassette.id_cassette] = Artiste.objects.filter(cassette=cassette)
    context = {
        "artiste": artiste,
        "cassettes": cassettes,
        "artistes": artistes
    }
    return render(
        request,
        "ttt_front/artiste_detail.html",
        context=context
    )

def events(request):
    events = Event.objects.all().order_by("-date_event")
    paginator = Paginator(events, 20)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = { 
        "page": page
    }
    return render(
        request,
        "ttt_front/event.html",
        context=context
    )

def event_detail(request, id_event):
    event = Event.objects.filter(id_event=id_event)
    context = {
        "event": event
    }
    return render(
        request,
        "ttt_front/event_detail.html",
        context=context
    )

def live_archives(request):
    return render(
        request,
        "ttt_front/live_archive.html"
    )

def links(request):
    artistes = Artiste.objects.all().values_list("nom", "lien_artiste")
    paginator = Paginator(artistes, 20)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page
    }
    return render(
        request,
        "ttt_front/link.html",
        context=context
    )

def contact(request):
    return render(
        request,
        "ttt_front/contact.html"
    )
