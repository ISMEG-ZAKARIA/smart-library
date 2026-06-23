from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Type(models.TextChoices):
        SYSTEME = "SYSTEM", "Système"
        RESERVATION = "RESERVATION", "Réservation"
        EMPRUNT = "LOAN", "Emprunt"
        RETOUR = "RETURN", "Retour"
        PENALITE = "PENALTY", "Pénalité"
        SECURITE = "SECURITY", "Sécurité"

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    journal_audit = models.ForeignKey(
        "audit.JournalAudit",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="notifications_generees",
    )
    type = models.CharField(max_length=15, choices=Type.choices, default=Type.SYSTEME)
    titre = models.CharField(max_length=160)
    message = models.TextField()
    lien = models.CharField(max_length=250, blank=True)
    creee_le = models.DateTimeField(auto_now_add=True, db_index=True)
    lue_le = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-creee_le"]
        indexes = [models.Index(fields=["utilisateur", "lue_le"], name="notification_user_lue_idx")]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(type="SYSTEM") | models.Q(journal_audit__isnull=False),
                name="notification_metier_auditee",
            )
        ]

    @property
    def est_lue(self):
        return self.lue_le is not None

    def __str__(self):
        return self.titre
