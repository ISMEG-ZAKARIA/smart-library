from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("connexion/", views.ConnexionView.as_view(), name="connexion"),
    path("deconnexion/", views.DeconnexionView.as_view(), name="deconnexion"),
    path("inscription/", views.inscription, name="inscription"),
    path("profil/", views.profil, name="profil"),
    path("parametres/", views.client_parametres, name="client_parametres"),
    path("admin/utilisateurs/", views.utilisateurs, name="utilisateurs"),
    path("admin/utilisateurs/nouveau/", views.utilisateur_form, name="utilisateur_nouveau"),
    path("admin/utilisateurs/<int:pk>/modifier/", views.utilisateur_form, name="utilisateur_modifier"),
    path("admin/utilisateurs/<int:pk>/blocage/", views.bloquer_utilisateur, name="utilisateur_blocage"),
    path("admin/statistiques/", views.statistiques, name="statistiques"),
    path("admin/parametres/", views.parametres, name="parametres"),
]
