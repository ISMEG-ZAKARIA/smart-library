from django.urls import path
from . import views

app_name = "alerts"
urlpatterns = [path("", views.liste, name="liste"), path("<int:pk>/lire/", views.lire, name="lire")]

