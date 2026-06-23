from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import ConfigurationBibliotheque, Utilisateur


class ConnexionForm(AuthenticationForm):
    username = forms.EmailField(label="Adresse e-mail")


class InscriptionForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ("username", "first_name", "last_name", "email", "cin", "telephone")


class UtilisateurForm(forms.ModelForm):
    mot_de_passe = forms.CharField(label="Mot de passe initial", widget=forms.PasswordInput, required=False, min_length=8)

    class Meta:
        model = Utilisateur
        fields = ("first_name", "last_name", "email", "cin", "telephone", "role", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["mot_de_passe"].required = True


class ProfilForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ("first_name", "last_name", "telephone", "notifications_email")


class ClientParametresForm(forms.ModelForm):
    """Préférences modifiables sans exposer l'identité enregistrée avec le CIN."""

    class Meta:
        model = Utilisateur
        fields = ("telephone", "notifications_email")


class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = ConfigurationBibliotheque
        exclude = ()
        widgets = {"modifie_le": forms.HiddenInput()}
