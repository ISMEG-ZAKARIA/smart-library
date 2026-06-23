from django.urls import path
from . import views

app_name = "reservations"
urlpatterns = [
    path("", views.liste, name="liste"),
    path("creer/<int:livre_id>/", views.creer, name="creer"),
    path("<int:pk>/annuler/", views.annuler, name="annuler"),
    path("suivi/", views.suivi, name="suivi"),
    path("<int:pk>/refuser/", views.refuser, name="refuser"),
]
