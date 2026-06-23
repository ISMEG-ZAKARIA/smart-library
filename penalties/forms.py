from django import forms
from accounts.models import Utilisateur
from .models import Penalite


class PenaliteForm(forms.ModelForm):
    class Meta:
        model = Penalite
        fields = ("client", "emprunt", "type", "motif", "montant")
        labels = {
            "client": "Client concerné",
            "emprunt": "Emprunt associé (facultatif)",
            "type": "Type de pénalité",
            "motif": "Motif détaillé",
            "montant": "Montant (DH)",
        }
        help_texts = {
            "client": "Seuls les comptes clients peuvent recevoir une pénalité.",
            "emprunt": "Sélectionnez un emprunt uniquement s'il est lié à cette pénalité.",
            "motif": "Décrivez précisément la raison de la pénalité.",
        }
        widgets = {
            "motif": forms.Textarea(attrs={"rows": 5, "placeholder": "Décrivez le motif de la pénalité…"}),
            "montant": forms.NumberInput(attrs={"min": "0", "step": "0.01", "placeholder": "0,00"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = Utilisateur.objects.filter(role=Utilisateur.Role.CLIENT).order_by(
            "last_name", "first_name", "email"
        )
        self.fields["client"].empty_label = "Sélectionner un client"
        self.fields["emprunt"].queryset = self.fields["emprunt"].queryset.select_related("client", "livre").order_by(
            "-emprunte_le", "-id"
        )
        self.fields["emprunt"].empty_label = "Aucun emprunt associé"

    def clean(self):
        donnees = super().clean()
        client = donnees.get("client")
        emprunt = donnees.get("emprunt")
        if client and emprunt and emprunt.client_id != client.id:
            raise forms.ValidationError("L'emprunt sélectionné n'appartient pas au client concerné.")
        return donnees
