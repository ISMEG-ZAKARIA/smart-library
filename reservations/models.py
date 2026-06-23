from django.conf import settings
from django.db import models
from .managers import ReservationQuerySet


class Reservation(models.Model):
    class Statut(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        CONVERTIE = "CONVERTED", "Convertie en emprunt"
        ANNULEE = "CANCELLED", "Annulée"
        EXPIREE = "EXPIRED", "Expirée"
        REFUSEE = "REFUSED", "Refusée"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    livre = models.ForeignKey("catalog.Livre", on_delete=models.PROTECT, related_name="reservations")
    statut = models.CharField(max_length=12, choices=Statut.choices, default=Statut.ACTIVE, db_index=True)
    reservee_le = models.DateTimeField(auto_now_add=True)
    expire_le = models.DateTimeField(db_index=True)
    annulee_le = models.DateTimeField(null=True, blank=True)
    motif_annulation = models.CharField(max_length=250, blank=True)
    traitee_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reservations_traitees",
    )
    traitee_le = models.DateTimeField(null=True, blank=True)
    motif_refus = models.CharField(max_length=250, blank=True)
    verrou_actif = models.BooleanField(null=True, default=True, editable=False)

    objects = ReservationQuerySet.as_manager()

    class Meta:
        ordering = ["-reservee_le"]
        indexes = [
            models.Index(fields=["client", "statut"]),
            models.Index(fields=["livre", "statut"]),
            models.Index(fields=["statut", "expire_le"], name="reservation_statut_exp_idx"),
        ]
        constraints = [
            models.UniqueConstraint(fields=["client", "livre", "verrou_actif"], name="reservation_active_unique"),
            models.CheckConstraint(condition=models.Q(expire_le__gt=models.F("reservee_le")), name="reservation_expiration_apres_creation"),
            models.CheckConstraint(
                condition=(
                    models.Q(statut="ACTIVE", verrou_actif=True)
                    | (~models.Q(statut="ACTIVE") & models.Q(verrou_actif__isnull=True))
                ),
                name="reservation_verrou_coherent",
            ),
            models.CheckConstraint(
                condition=(~models.Q(statut="CANCELLED") | models.Q(annulee_le__isnull=False)),
                name="reservation_annulation_datee",
            ),
            models.CheckConstraint(
                condition=(~models.Q(statut="REFUSED") | models.Q(traitee_le__isnull=False, traitee_par__isnull=False)),
                name="reservation_refus_trace",
            ),
        ]

    def __str__(self):
        return f"{self.client} — {self.livre}"
