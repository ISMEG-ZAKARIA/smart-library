from django.db import models
from django.utils import timezone


class ReservationQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(statut="ACTIVE", expire_le__gt=timezone.now())

    def a_expirer(self):
        return self.filter(statut="ACTIVE", expire_le__lte=timezone.now())

