from django.urls import path
from . import views

app_name = "penalties"
urlpatterns = [
    path("", views.liste, name="liste"),
    path("creer/", views.creer, name="creer"),
    path("<int:pk>/regler/", views.regler, name="regler"),
    path("<int:pk>/annuler/", views.annuler, name="annuler"),
]
