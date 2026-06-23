from django.contrib import admin
from .models import Emprunt


@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ("client", "livre", "statut", "emprunte_le", "retour_prevu_le", "retourne_le")
    list_filter = ("statut", "etat_retour")
    search_fields = ("client__email", "livre__titre")

