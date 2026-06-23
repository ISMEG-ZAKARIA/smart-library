from django.urls import path
from . import views

app_name = "loans"
urlpatterns = [
    path("validations/", views.validations, name="validations"),
    path("valider/<int:reservation_id>/", views.valider, name="valider"),
    path("retours/", views.retours, name="retours"),
    path("retours/<int:pk>/", views.retour, name="retour"),
    path("historique/", views.historique, name="historique"),
    path("suivi/", views.suivi, name="suivi"),
]
