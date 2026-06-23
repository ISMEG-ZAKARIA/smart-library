from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("client", "livre", "statut", "reservee_le", "expire_le")
    list_filter = ("statut",)
    search_fields = ("client__email", "livre__titre")

