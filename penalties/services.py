from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .models import Penalite


@transaction.atomic
def creer_penalite(client, emprunt, type_penalite, montant, motif, acteur):
    """Crée une pénalité et recalcule immédiatement le risque du client."""
    from abuse.services import evaluer_niveau_risque
    from audit.services import journaliser
    from alerts.services import notifier

    if not client.est_client:
        raise ValidationError("Une pénalité doit être liée à un compte client.")
    if emprunt and emprunt.client_id != client.id:
        raise ValidationError("L'emprunt sélectionné n'appartient pas au client concerné.")
    penalite = Penalite.objects.create(client=client, emprunt=emprunt, type=type_penalite, montant=montant, motif=motif, creee_par=acteur)
    evaluer_niveau_risque(client)
    audit = journaliser(acteur, "PENALITE_CREEE", penalite, {"montant": str(montant), "type": type_penalite})
    notifier(client, "Nouvelle pénalité", f"Une pénalité de {montant} DH a été appliquée : {motif}", "PENALTY", "/penalites/", journal_audit=audit)
    return penalite


@transaction.atomic
def regler_penalite(penalite, acteur):
    """Clôture une pénalité ouverte et met à jour le profil de risque."""
    from abuse.services import evaluer_niveau_risque
    from audit.services import journaliser
    from alerts.services import notifier

    penalite = Penalite.objects.select_for_update().select_related("client").get(pk=penalite.pk)
    if penalite.statut != Penalite.Statut.OUVERTE:
        raise ValidationError("Cette pénalité n'est plus ouverte.")
    penalite.statut = Penalite.Statut.REGLEE
    penalite.reglee_le = timezone.now()
    penalite.save(update_fields=["statut", "reglee_le"])
    evaluer_niveau_risque(penalite.client)
    audit = journaliser(acteur, "PENALITE_REGLEE", penalite)
    notifier(penalite.client, "Pénalité réglée", f"La pénalité de {penalite.montant} DH est clôturée.", "PENALTY", journal_audit=audit)
    return penalite


@transaction.atomic
def annuler_penalite(penalite, acteur, motif):
    """Annule sans supprimer l'historique, puis synchronise risque, notification et audit."""
    from abuse.services import evaluer_niveau_risque
    from audit.services import journaliser
    from alerts.services import notifier

    penalite = Penalite.objects.select_for_update().select_related("client").get(pk=penalite.pk)
    if penalite.statut != Penalite.Statut.OUVERTE:
        raise ValidationError("Seule une pénalité ouverte peut être annulée.")
    penalite.statut = Penalite.Statut.ANNULEE
    penalite.motif = f"{penalite.motif}\nAnnulation : {motif}"
    penalite.save(update_fields=["statut", "motif"])
    evaluer_niveau_risque(penalite.client)
    audit = journaliser(acteur, "PENALITE_ANNULEE", penalite, {"motif": motif})
    notifier(penalite.client, "Pénalité annulée", f"La pénalité de {penalite.montant} DH a été annulée : {motif}", "PENALTY", "/penalites/", journal_audit=audit)
    return penalite
