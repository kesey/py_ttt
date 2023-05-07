from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from ttt_front.models import Cassette
from ttt_back.models import Exemplaire, EtatExemplaire, ComptaVendeur
from ttt_back.forms import VenteRapideForm
from authentication.models import User
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.db.models import Sum, Q
import datetime

@login_required
def gestion_exemplaire(request, *args, **kwargs): # create a custom admin view
    cassette_obj = Cassette.objects
    message = ""
    if request.GET.get("search_query"): # search query
        query = request.GET.get("search_query")
        search_results = cassette_obj.filter(
            Q(titre__icontains=query) | 
            Q(code__icontains=query) | 
            Q(date_sortie__icontains=query) | 
            Q(description__icontains=query) | 
            Q(longueur__icontains=query)
        )
        search_results = search_results.order_by("-date_sortie")
        if not search_results:
            message = "Aucun résultat trouvé"
    else:
        search_results = ""
    cassettes = cassette_obj.all().order_by("-date_sortie")
    paginator = Paginator(cassettes, 15)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = { 
        "page": page,
        "search_results": search_results,
        "message": message
    }
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
            exemplaires_stat[etat.description_etat.replace("-", "_")] = exemplaires.filter(id_etat_exemplaire=etat.id_etat_exemplaire).count()
        exemplaires_stat["ventes_totales"] = exemplaires.aggregate(ventes_totales = Sum("prix_vente_euros"))["ventes_totales"]
        exemplaires_stat["ventes_totales"] = exemplaires_stat["ventes_totales"] if exemplaires_stat["ventes_totales"] else 0
        total_fdp = exemplaires.aggregate(fdp_total = Sum("montant_frais_de_port"))["fdp_total"]
        total_fdp = total_fdp if total_fdp else 0
        exemplaires_stat["gains_reels"] = exemplaires_stat["ventes_totales"] - total_fdp
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
    
class Vente_rapide(LoginRequiredMixin, View):
    template_name = "ttt_back/vente_rapide.html"
    form_class = VenteRapideForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'prix_vente_euros': 6.00, 'vente_rembousee': False, 'commentaire': f"vente rapide de { request.user.first_name }"})
        return render(
            request,
            self.template_name,
            { "form": form }
        )
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            exemplaires = Exemplaire.objects.filter(
                Q(id_cassette=form.cleaned_data['id_cassette'].id_cassette) & 
                Q(id_etat_exemplaire=1)
            )
            exemplaire = exemplaires.first()
            if exemplaire:
                exemplaire.id_vendeur = request.user
                etat = EtatExemplaire.objects.filter(id_etat_exemplaire=2)
                exemplaire.id_etat_exemplaire = etat.get()
                exemplaire.date_vente = datetime.datetime.now().strftime("%Y-%m-%d")
                exemplaire.prix_vente_euros = form.cleaned_data['prix_vente_euros']
                exemplaire.vente_remboursee = form.cleaned_data['vente_remboursee']
                exemplaire.commentaire = form.cleaned_data['commentaire']
                # exemplaire.save()
                message = "Exemplaire vendu"
            else:
                cassette = Cassette.objects.filter(id_cassette=form.cleaned_data['id_cassette'].id_cassette)
                cassette = cassette.get()
                if not cassette.sold_out:
                    cassette.sold_out = True
                    cassette.save()
                message = "Il n'y a plus d'exemplaire disponible"
        else:
            message = "formulaire invalide"
        context = { 
            "form": form,
            "message": message
        }
        return render(
            request,
            self.template_name,
            context=context
        )

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
        order = "numero_exemplaire"
        if request.GET.get("order_list"): # change order of exemplaire table
            order = request.GET.get("order_list")
        exemplaires = Exemplaire.objects.filter(id_cassette=kwargs["id_cassette"]).order_by(order)
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
                    message = "tableau d'exemplaires sauvegardé"
        else:
            message = "données invalides"
        exemplaires_stat = Calcul().exemplaires_stat(exemplaires)
        if not exemplaires_stat["en_stock"]: # if no exemplaire left the cassette is sold out
            cassette = Cassette.objects.filter(id_cassette=kwargs["id_cassette"])
            cassette = cassette.get()
            if not cassette.sold_out:
                cassette.sold_out = True
                cassette.save()
        vendeurs_stat = Calcul().vendeurs_stat(exemplaires)
        cassette_stat = Calcul().cassette_stat(kwargs["id_cassette"])
        context = {
            "formset": exemplaires_formset,
            "vendeurs_stat": vendeurs_stat,
            "exemplaires_stat": exemplaires_stat,
            "cassette_stat": cassette_stat,
            "message": message
        }
        return render(
            request,
            self.template_name,
            context
        )