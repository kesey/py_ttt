from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from ttt_front.models import Cassette
from ttt_back.models import Exemplaire
from django.core.paginator import Paginator
from django.forms import modelformset_factory

@login_required
def gestion_exemplaire(request, *args, **kwargs): # create a custom admin view
    cassettes = Cassette.objects.all().order_by("-date_sortie")
    paginator = Paginator(cassettes, 20)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = { "page": page }
    return render(
        request,
        "ttt_back/gestion_exemplaire.html",
        context=context
    )

class Compta(LoginRequiredMixin, View):
    template_name = "ttt_back/compta.html"

    def get(self, request, **kwargs): # use **kwargs to get url parameters
        return render(
            request,
            self.template_name
        )
    
    def post(self, request, **kwargs):
        return render(
            request,
            self.template_name
        )

class Gestion_exemplaire_detail(LoginRequiredMixin, View):
    template_name = "ttt_back/gestion_exemplaire_detail.html"

    def get(self, request, **kwargs): # use **kwargs to get url parameters
        exemplaires_formset = modelformset_factory(Exemplaire, exclude=["id_cassette"])
        exemplaires_formset = exemplaires_formset(queryset=Exemplaire.objects.filter(id_cassette=kwargs["id_cassette"]))
        return render(
            request,
            self.template_name,
            { "formset": exemplaires_formset }
        )
    
    def post(self, request, **kwargs):
        return render(
            request,
            self.template_name
        )