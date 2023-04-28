from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from ttt_front.models import Cassette
from ttt_back.models import Exemplaire, EtatExemplaire, ComptaVendeur
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

class Calcul:
    def exemplaires_stat(self, exemplaires):
        etats = EtatExemplaire.objects.all()
        exemplaires_stat = {}
        for etat in etats:
            exemplaires_stat[etat.description_etat.replace("-", "_")] = exemplaires.filter(id_etat=etat.id_etat_exemplaire).count()
        exemplaires_stat["ventes_totales"] = exemplaires.aggregate(ventes_totales = Sum("prix_vente_euros"))["ventes_totales"]
        exemplaires_stat["gains_reels"] = exemplaires_stat["ventes_totales"] - exemplaires.aggregate(gains_reels = Sum("montant_frais_de_port"))["gains_reels"]
        return exemplaires_stat

    def vendeurs_stat(self, exemplaires):
        vendeurs = User.objects.all()
        vendeurs_stat = {}
        for vendeur in vendeurs:
            exemplaires_vendeur = exemplaires.filter(id_vendeur=vendeur.id)
            vendeurs_stat[vendeur.first_name] = exemplaires_vendeur.aggregate(a_vendu_pour = Sum("prix_vente_euros"))
            vendeurs_stat[vendeur.first_name]["doit"] = exemplaires_vendeur.exclude(vente_remboursee=1).aggregate(doit = Sum("prix_vente_euros"))["doit"]
            vendeurs_stat[vendeur.first_name]["doit_recup"] = exemplaires_vendeur.exclude(frais_de_port_rembourses=1).aggregate(doit_recup = Sum("montant_frais_de_port"))["doit_recup"]
        return vendeurs_stat
    
    def compta_vendeurs_stat(self, exemplaires):
        vendeurs = User.objects.all()
        vendeurs_stat = {}
        for vendeur in vendeurs:
            exemplaires_vendeur = exemplaires.filter(id_vendeur=vendeur.id)

            compta_vendeur = ComptaVendeur.objects.filter(id_vendeur=vendeur.id).aggregate(a_rembourse = Sum("a_rembourse"), a_recupere = Sum("a_recupere"))
            compta_vendeur["a_rembourse"] = compta_vendeur["a_rembourse"] if compta_vendeur["a_rembourse"] else 0
            compta_vendeur["a_recupere"] = compta_vendeur["a_recupere"] if compta_vendeur["a_recupere"] else 0

            vendeurs_stat[vendeur.first_name] = exemplaires_vendeur.aggregate(a_vendu_pour = Sum("prix_vente_euros"))
            vendeurs_stat[vendeur.first_name]["doit"] = exemplaires_vendeur.exclude(vente_remboursee=1).aggregate(doit = Sum("prix_vente_euros"))["doit"]
            vendeurs_stat[vendeur.first_name]["doit_recup"] = exemplaires_vendeur.exclude(frais_de_port_rembourses=1).aggregate(doit_recup = Sum("montant_frais_de_port"))["doit_recup"]
            
            vendeurs_stat[vendeur.first_name]["doit"] = vendeurs_stat[vendeur.first_name]["doit"] if vendeurs_stat[vendeur.first_name]["doit"] else 0
            vendeurs_stat[vendeur.first_name]["doit"] = vendeurs_stat[vendeur.first_name]["doit"] - compta_vendeur["a_rembourse"]
            
            vendeurs_stat[vendeur.first_name]["doit_recup"] = vendeurs_stat[vendeur.first_name]["doit_recup"] if vendeurs_stat[vendeur.first_name]["doit_recup"] else 0
            vendeurs_stat[vendeur.first_name]["doit_recup"] = vendeurs_stat[vendeur.first_name]["doit_recup"] - compta_vendeur["a_recupere"]
        return vendeurs_stat

    def cassettes_stat(self):
        cassettes_stat = Cassette.objects.all().aggregate(nombre_de_download = Sum("nombre_de_download"))
        return cassettes_stat

    def cassette_stat(self, id_cassette):
        cassette = Cassette.objects.filter(id_cassette=id_cassette).values_list("nombre_de_download", "code", "titre")[0]
        cassette_stat = {}
        cassette_stat["nombre_de_download"] = cassette[0]
        cassette_stat["code"] = cassette[1]
        cassette_stat["titre"] = cassette[2]
        return cassette_stat

@login_required
def compta(request, *args, **kwargs):
    exemplaires = Exemplaire.objects.all()
    exemplaires_stat = Calcul().exemplaires_stat(exemplaires)
    vendeurs_stat = Calcul().compta_vendeurs_stat(exemplaires)
    cassettes_stat = Calcul().cassettes_stat()

    context = {
        "vendeurs_stat": vendeurs_stat,
        "exemplaires_stat": exemplaires_stat,
        "cassette_stat": cassettes_stat
    }
    return render(
        request,
        "ttt_back/compta.html",
        context
    )

class Gestion_exemplaire_detail(LoginRequiredMixin, View):
    template_name = "ttt_back/gestion_exemplaire_detail.html"
    exemplaires_formset = modelformset_factory(Exemplaire, exclude=["id_cassette"])
    
    def get(self, request, **kwargs): # use **kwargs to get url parameters
        exemplaires = Exemplaire.objects.filter(id_cassette=kwargs["id_cassette"])
        exemplaires_formset = self.exemplaires_formset(queryset=exemplaires)
        exemplaires_stat = Calcul().exemplaires_stat(exemplaires)
        vendeurs_stat = Calcul().vendeurs_stat(exemplaires)
        cassette_stat = Calcul().cassette_stat(kwargs["id_cassette"])
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
        exemplaires_stat = Calcul().exemplaires_stat(exemplaires)
        if not exemplaires_stat.en_stock: # if no exemplaires left the cassette is sold out
            cassette = Cassette.objects.filter(id_cassette=kwargs["id_cassette"])
            if not cassette.sold_out:
                cassette.sold_out = True
                cassette.save()
        vendeurs_stat = Calcul().vendeurs_stat(exemplaires)
        cassette_stat = Calcul().cassette_stat(kwargs["id_cassette"])
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