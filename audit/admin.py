from django.contrib import admin
from .models import JournalAudit


@admin.register(JournalAudit)
class JournalAuditAdmin(admin.ModelAdmin):
    list_display = ("cree_le", "action", "acteur", "cible_type", "description_cible")
    list_filter = ("action", "cible_type")
    search_fields = ("action", "description_cible", "acteur__email")
    readonly_fields = ("acteur", "action", "cible_type", "cible_id", "description_cible", "details", "adresse_ip", "cree_le")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

