from django import forms


class AnnulationReservationForm(forms.Form):
    motif = forms.CharField(max_length=250, initial="Annulation demandée par le client", widget=forms.Textarea(attrs={"rows": 2}))

