from django import forms
from .models import Emprunt


class ValidationEmpruntForm(forms.Form):
    reservation_id = forms.IntegerField(widget=forms.HiddenInput())
    code_qr = forms.CharField(label="Code QR scanné", max_length=50)


class RetourForm(forms.Form):
    code_qr = forms.CharField(label="Code QR scanné", max_length=50)
    poids_retour_grammes = forms.IntegerField(label="Poids mesuré (g)", min_value=1)
    etat_retour = forms.ChoiceField(label="État constaté", choices=Emprunt.EtatRetour.choices)
    commentaire_retour = forms.CharField(label="Observation", required=False, widget=forms.Textarea(attrs={"rows": 3}))

