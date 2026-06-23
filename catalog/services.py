from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Livre


@transaction.atomic
def enregistrer_livre(form, acteur):
    """Enregistre un ouvrage, recalcule son statut et journalise la modification."""
    from audit.services import journaliser

    creation = form.instance.pk is None
    livre = form.save()
    livre.actualiser_statut()
    journaliser(acteur, "LIVRE_AJOUTE" if creation else "LIVRE_MODIFIE", livre, {"isbn": livre.isbn, "stock": livre.stock_total})
    return livre


@transaction.atomic
def placer_en_maintenance(livre_id, acteur, motif):
    """Retire immédiatement un ouvrage endommagé du catalogue disponible."""
    from audit.services import journaliser

    livre = Livre.objects.select_for_update().get(pk=livre_id)
    livre.statut = Livre.Statut.MAINTENANCE
    livre.save(update_fields=["statut", "modifie_le"])
    journaliser(acteur, "LIVRE_MAINTENANCE", livre, {"motif": motif})
    return livre


@transaction.atomic
def desactiver_livre(livre_id, acteur, motif):
    """Retire un livre des catalogues sans détruire son historique relationnel."""
    from audit.services import journaliser

    livre = Livre.objects.select_for_update().get(pk=livre_id)
    if livre.reservations.filter(statut="ACTIVE").exists() or livre.emprunts.filter(statut__in=["ACTIVE", "INSPECTION"]).exists():
        raise ValidationError("Le livre possède une réservation ou un emprunt actif.")
    livre.actif = False
    livre.statut = Livre.Statut.INDISPONIBLE
    livre.save(update_fields=["actif", "statut", "modifie_le"])
    journaliser(acteur, "LIVRE_RETIRE", livre, {"motif": motif})
    return livre
