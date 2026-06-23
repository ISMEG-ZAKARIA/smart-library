from django.conf import settings
from django.db import models
from .managers import EmpruntQuerySet


class Emprunt(models.Model):
    class Statut(models.TextChoices):
        EN_COURS = "ACTIVE", "En cours"
        RETOURNE = "RETURNED", "Retourné"
        INSPECTION = "INSPECTION", "En inspection"

    class EtatRetour(models.TextChoices):
        BON = "GOOD", "Bon état"
        ENDOMMAGE = "DAMAGED", "Endommagé"
        PERDU = "LOST", "Perdu"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="emprunts")
    livre = models.ForeignKey("catalog.Livre", on_delete=models.PROTECT, related_name="emprunts")
    reservation = models.OneToOneField("reservations.Reservation", null=True, blank=True, on_delete=models.PROTECT, related_name="emprunt")
    valide_par = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="emprunts_valides")
    emprunte_le = models.DateField()
    retour_prevu_le = models.DateField(db_index=True)
    retourne_le = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=12, choices=Statut.choices, default=Statut.EN_COURS, db_index=True)
    etat_retour = models.CharField(max_length=10, choices=EtatRetour.choices, blank=True)
    poids_retour_grammes = models.PositiveIntegerField(null=True, blank=True)
    commentaire_retour = models.TextField(blank=True)

    objects = EmpruntQuerySet.as_manager()

    class Meta:
        ordering = ["-emprunte_le", "-id"]
        indexes = [
            models.Index(fields=["client", "statut"]),
            models.Index(fields=["livre", "statut"]),
            models.Index(fields=["statut", "retour_prevu_le"], name="emprunt_statut_echeance_idx"),
        ]
        constraints = [
            models.CheckConstraint(condition=models.Q(retour_prevu_le__gte=models.F("emprunte_le")), name="emprunt_echeance_valide"),
            models.CheckConstraint(
                condition=models.Q(retourne_le__isnull=True) | models.Q(retourne_le__gte=models.F("emprunte_le")),
                name="emprunt_retour_apres_debut",
            ),
            models.CheckConstraint(
                condition=~models.Q(statut="RETURNED") | models.Q(retourne_le__isnull=False),
                name="emprunt_termine_date_retour",
            ),
        ]

    def __str__(self):
        return f"{self.client} — {self.livre}"

    @property
    def jours_retard(self):
        from django.utils import timezone

        fin = self.retourne_le or timezone.localdate()
        return max(0, (fin - self.retour_prevu_le).days)
