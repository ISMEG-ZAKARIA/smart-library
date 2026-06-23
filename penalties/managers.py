from django.db import models


class PenaliteQuerySet(models.QuerySet):
    def ouvertes(self):
        return self.filter(statut="OPEN")

