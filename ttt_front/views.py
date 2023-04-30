from django.shortcuts import render, redirect
from ttt_front.models import Cassette, Artiste, Event, FraisDePort
from django.core.paginator import Paginator
from django.http import FileResponse
from django.conf import settings
import pathlib

def label(request):
    return render(
        request,
        "ttt_front/label.html"
    )

def home(request):
    cassettes = Cassette.objects.all().exclude(publier=0).order_by("-date_sortie")
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

def download(request, id_cassette):
    cassette = Cassette.objects.filter(id_cassette=id_cassette)
    cassette = cassette.get()
    file_name = str(cassette.download)
    file_server = pathlib.Path(str(settings.MEDIA_ROOT) + "/" + file_name)
    if file_server.exists():
        nb_dl = cassette.nombre_de_download + 1
        cassette.nombre_de_download = nb_dl
        cassette.save()
        file_to_download = open(file_server, 'rb')
        file_name = file_name.split("/")[-1]
        response = FileResponse(file_to_download, filename=file_name, content_type='application/force-download')
        response['Content-Disposition'] = f'inline; filename="{ file_name }"'
        return response
    else:
        return redirect(request.META['HTTP_REFERER'])

def artistes(request):
    artistes = Artiste.objects.all().exclude(publier=0).order_by("-id_artiste")
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
    events = Event.objects.all().exclude(publier=0).order_by("-date_event")
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
    artistes = Artiste.objects.all().exclude(publier=0).values_list("nom", "lien_artiste")
    paginator = Paginator(artistes, 15)
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
