from django import forms
from .models import Commentaire, Livre


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ("titre", "isbn", "auteurs", "categorie", "description", "annee_publication", "editeur", "poids_reference_grammes", "tolerance_poids_grammes", "couverture", "visible_client", "stock_total", "stock_disponible", "actif")
        widgets = {"auteurs": forms.SelectMultiple(attrs={"size": 5}), "description": forms.Textarea(attrs={"rows": 4})}


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ("note", "texte")
