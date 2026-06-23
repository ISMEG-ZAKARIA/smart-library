from django.conf import settings
from django.db import models


class JournalAudit(models.Model):
    acteur = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="actions_audit")
    action = models.CharField(max_length=80, db_index=True)
    cible_type = models.CharField(max_length=100)
    cible_id = models.CharField(max_length=80)
    description_cible = models.CharField(max_length=250, blank=True)
    details = models.JSONField(default=dict, blank=True)
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-cree_le"]
        verbose_name = "entrée du journal d'audit"
        indexes = [
            models.Index(fields=["action", "cree_le"], name="audit_action_date_idx"),
            models.Index(fields=["acteur", "cree_le"], name="audit_acteur_date_idx"),
            models.Index(fields=["cible_type", "cible_id"], name="audit_cible_idx"),
        ]

    def __str__(self):
        return f"{self.action} — {self.description_cible}"
