from django.urls import path
from . import views

app_name = "catalog"
urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path("ajouter/", views.livre_form, name="ajouter"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/modifier/", views.livre_form, name="modifier"),
    path("<int:pk>/desactiver/", views.desactiver, name="desactiver"),
]
