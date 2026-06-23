from django.contrib import admin
from .models import Auteur, Categorie, Commentaire, Livre


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ("titre", "isbn", "categorie", "stock_disponible", "stock_total", "statut", "visible_client")
    list_filter = ("statut", "categorie", "actif", "visible_client")
    search_fields = ("titre", "isbn", "auteurs__nom")
    filter_horizontal = ("auteurs",)


admin.site.register(Auteur)
admin.site.register(Categorie)
admin.site.register(Commentaire)
