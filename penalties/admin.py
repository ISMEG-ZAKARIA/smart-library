from django.contrib import admin
from .models import Penalite


@admin.register(Penalite)
class PenaliteAdmin(admin.ModelAdmin):
    list_display = ("client", "type", "montant", "statut", "creee_le")
    list_filter = ("type", "statut")
    search_fields = ("client__email", "motif")

