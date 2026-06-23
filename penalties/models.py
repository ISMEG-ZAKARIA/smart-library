from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from .managers import PenaliteQuerySet


class Penalite(models.Model):
    class Type(models.TextChoices):
        RETARD = "LATE", "Retard"
        DOMMAGE = "DAMAGE", "Dommage"
        PERTE = "LOSS", "Perte"
        AUTRE = "OTHER", "Autre"

    class Statut(models.TextChoices):
        OUVERTE = "OPEN", "Ouverte"
        REGLEE = "PAID", "Réglée"
        ANNULEE = "CANCELLED", "Annulée"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="penalites")
    emprunt = models.ForeignKey("loans.Emprunt", null=True, blank=True, on_delete=models.PROTECT, related_name="penalites")
    type = models.CharField(max_length=10, choices=Type.choices)
    motif = models.TextField()
    montant = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    statut = models.CharField(max_length=10, choices=Statut.choices, default=Statut.OUVERTE, db_index=True)
    creee_par = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="penalites_creees")
    creee_le = models.DateTimeField(auto_now_add=True)
    reglee_le = models.DateTimeField(null=True, blank=True)

    objects = PenaliteQuerySet.as_manager()

    class Meta:
        ordering = ["-creee_le"]
        indexes = [
            models.Index(fields=["client", "statut"], name="penalite_client_statut_idx"),
            models.Index(fields=["type", "statut"], name="penalite_type_statut_idx"),
        ]
        constraints = [
            models.CheckConstraint(condition=models.Q(montant__gte=0), name="penalite_montant_positif"),
            models.CheckConstraint(
                condition=~models.Q(statut="PAID") | models.Q(reglee_le__isnull=False),
                name="penalite_reglee_datee",
            ),
        ]

    def __str__(self):
        return f"{self.get_type_display()} — {self.client} — {self.montant} DH"
