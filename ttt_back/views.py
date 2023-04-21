from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from ttt_front.models import Cassette
from ttt_back.models import Exemplaire, EtatExemplaire
from authentication.models import User
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.db.models import Sum

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
    exemplaires_formset = modelformset_factory(Exemplaire, exclude=["id_cassette"])
    
    def exemplaires_stat(self, exemplaires):
        etats = EtatExemplaire.objects.all()
        exemplaires_stat = {}
        for etat in etats:
            exemplaires_stat[etat.description_etat] = exemplaires.filter(id_etat=etat.id_etat_exemplaire).count()
        exemplaires_stat["ventes_totales"] = exemplaires.aggregate(ventes_totales = Sum("prix_vente_euros"))["ventes_totales"]
        exemplaires_stat["gains_reels"] = exemplaires_stat["ventes_totales"] - exemplaires.aggregate(gains_reels = Sum("montant_frais_de_port"))["gains_reels"]
        return exemplaires_stat
    
    def vendeurs_stat(self, exemplaires):
        vendeurs = User.objects.filter(suppr=0)
        vendeurs_stat = {}
        for vendeur in vendeurs:
            exemplaires_vendeur = exemplaires.filter(id_vendeur=vendeur.id)
            vendeurs_stat[vendeur.first_name] = exemplaires_vendeur.aggregate(a_vendu_pour = Sum("prix_vente_euros"))
            vendeurs_stat[vendeur.first_name]["doit"] = exemplaires_vendeur.exclude(vente_remboursee=1).aggregate(doit = Sum("prix_vente_euros"))["doit"]
            vendeurs_stat[vendeur.first_name]["doit_recup"] = exemplaires_vendeur.exclude(frais_de_port_rembourses=1).aggregate(doit_recup = Sum("montant_frais_de_port"))["doit_recup"]
        return vendeurs_stat
    
    def cassette_stat(self, id_cassette):
        return Cassette.objects.filter(id_cassette=id_cassette).values("nombre_de_download")[0]

    def get(self, request, **kwargs): # use **kwargs to get url parameters
        exemplaires = Exemplaire.objects.filter(id_cassette=kwargs["id_cassette"])
        exemplaires_formset = self.exemplaires_formset(queryset=exemplaires)
        exemplaires_stat = self.exemplaires_stat(exemplaires)
        vendeurs_stat = self.vendeurs_stat(exemplaires)
        cassette_stat = self.cassette_stat(kwargs["id_cassette"])
        context = {
            "formset": exemplaires_formset,
            "vendeurs_stat": vendeurs_stat,
            "exemplaires_stat": exemplaires_stat,
            "cassette_stat": cassette_stat
        }
        return render(
            request,
            self.template_name,
            context
        )
    
    def post(self, request, **kwargs):
        exemplaires = Exemplaire.objects.filter(id_cassette=kwargs["id_cassette"])
        exemplaires_formset = self.exemplaires_formset(request.POST, queryset=exemplaires)
        if exemplaires_formset.is_valid():
            for form in exemplaires_formset:
                if form.cleaned_data:
                    form.save()
        exemplaires_stat = self.exemplaires_stat(exemplaires)
        vendeurs_stat = self.vendeurs_stat(exemplaires)
        cassette_stat = self.cassette_stat(kwargs["id_cassette"])
        context = {
            "formset": exemplaires_formset,
            "vendeurs_stat": vendeurs_stat,
            "exemplaires_stat": exemplaires_stat,
            "cassette_stat": cassette_stat
        }
        return render(
            request,
            self.template_name,
            context
        )