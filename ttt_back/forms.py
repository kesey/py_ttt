from django import forms
from ttt_back.models import Exemplaire, Cassette

class VenteRapideForm(forms.ModelForm):
    id_cassette = forms.ModelChoiceField(
        queryset=Cassette.objects.filter(sold_out=False).order_by("-date_sortie")
    ) # filter possible choices in select input
    nombres_exemplaires = forms.IntegerField(initial=1)

    class Meta:
        model = Exemplaire
        fields = ('id_cassette', 'prix_vente_euros', 'vente_remboursee', 'commentaire')
        labels = { # create custom name for display in template
            "prix_vente_euros": "Prix de vente (Euros)",
            "vente_remboursee": "Vente remboursée",
            "commentaire": "Commentaire"
        }