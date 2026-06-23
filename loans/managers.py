from django.db import models
from django.utils import timezone


class EmpruntQuerySet(models.QuerySet):
    def actifs(self):
        return self.filter(statut="ACTIVE")

    def en_retard(self):
        return self.filter(statut="ACTIVE", retour_prevu_le__lt=timezone.localdate())

