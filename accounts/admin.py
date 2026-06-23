from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ConfigurationBibliotheque, Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ("email", "username", "role", "est_bloque", "niveau_alerte", "is_active")
    list_filter = ("role", "est_bloque", "is_active")
    search_fields = ("email", "username", "cin", "first_name", "last_name")
    fieldsets = UserAdmin.fieldsets + (("Smart Library", {"fields": ("cin", "telephone", "role", "niveau_alerte", "score_risque", "est_bloque", "deux_facteurs_actif", "notifications_email")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Smart Library", {"fields": ("email", "cin", "role")}),)


admin.site.register(ConfigurationBibliotheque)
