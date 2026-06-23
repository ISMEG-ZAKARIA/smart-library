from django import forms
from accounts.models import Utilisateur
from .models import Restriction


class RestrictionForm(forms.Form):
    utilisateur = forms.ModelChoiceField(queryset=Utilisateur.objects.filter(role=Utilisateur.Role.CLIENT), label="Utilisateur")
    type = forms.ChoiceField(choices=Restriction.Type.choices, label="Type de restriction")
    motif = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="Motif / justification")
    duree_jours = forms.IntegerField(min_value=1, max_value=365, initial=30, label="Durée (jours)")

