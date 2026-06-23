from django.conf import settings
from django.db import models


class RapportAbus(models.Model):
    class Severite(models.TextChoices):
        FAIBLE = "LOW", "Faible"
        MOYENNE = "MEDIUM", "Moyenne"
        ELEVEE = "HIGH", "Élevée"
        CRITIQUE = "CRITICAL", "Critique"

    class Statut(models.TextChoices):
        OUVERT = "OPEN", "Ouvert"
        TRAITE = "RESOLVED", "Traité"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rapports_abus")
    type_alerte = models.CharField(max_length=50)
    severite = models.CharField(max_length=10, choices=Severite.choices, default=Severite.MOYENNE, db_index=True)
    description = models.TextField()
    source_type = models.CharField(max_length=100, blank=True)
    source_id = models.CharField(max_length=80, blank=True)
    statut = models.CharField(max_length=10, choices=Statut.choices, default=Statut.OUVERT, db_index=True)
    traite_par = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="abus_traites")
    cree_le = models.DateTimeField(auto_now_add=True, db_index=True)
    traite_le = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-cree_le"]
        indexes = [
            models.Index(fields=["client", "statut"], name="abus_client_statut_idx"),
            models.Index(fields=["severite", "statut"], name="abus_severite_statut_idx"),
        ]

    def __str__(self):
        return f"{self.type_alerte} — {self.client}"


class Restriction(models.Model):
    class Type(models.TextChoices):
        EMPRUNTS = "LOANS", "Suspension temporaire des emprunts"
        COMPTE = "ACCOUNT", "Blocage du compte"
        AVERTISSEMENT = "WARNING", "Avertissement formel"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restrictions")
    type = models.CharField(max_length=10, choices=Type.choices)
    motif = models.TextField()
    debut = models.DateTimeField(auto_now_add=True)
    fin = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True, db_index=True)
    appliquee_par = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="restrictions_appliquees")

    class Meta:
        ordering = ["-debut"]
        indexes = [models.Index(fields=["client", "active", "fin"], name="restriction_client_active_idx")]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(fin__isnull=True) | models.Q(fin__gt=models.F("debut")),
                name="restriction_fin_apres_debut",
            )
        ]

    def __str__(self):
        return f"{self.get_type_display()} — {self.client}"
