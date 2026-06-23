from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from .models import RapportAbus, Restriction


def creer_rapport_abus(client, type_alerte, description, source=None, severite="MEDIUM"):
    """Centralise une anomalie avec une référence vers son objet métier d'origine."""
    return RapportAbus.objects.create(
        client=client,
        type_alerte=type_alerte,
        description=description,
        severite=severite,
        source_type=source._meta.label if source else "",
        source_id=str(source.pk) if source else "",
    )


@transaction.atomic
def evaluer_niveau_risque(client):
    """Calcule le risque ; trois alertes ou un score critique bloquent le client."""
    from penalties.models import Penalite

    alertes = client.niveau_alerte
    rapports_graves = client.rapports_abus.filter(statut=RapportAbus.Statut.OUVERT, severite__in=[RapportAbus.Severite.ELEVEE, RapportAbus.Severite.CRITIQUE]).count()
    penalites_ouvertes = client.penalites.filter(statut=Penalite.Statut.OUVERTE).count()
    score = min(100, alertes * 25 + rapports_graves * 25 + penalites_ouvertes * 10)
    client.score_risque = score
    if alertes >= 3 or score >= 75:
        client.est_bloque = True
        client.is_active = False
    client.save(update_fields=["score_risque", "est_bloque", "is_active"])
    return score


@transaction.atomic
def appliquer_restriction(client, type_restriction, motif, duree_jours, acteur):
    """Applique une restriction, notifie le client et laisse une trace d'audit."""
    from audit.services import journaliser
    from alerts.services import notifier

    restriction = Restriction.objects.create(
        client=client,
        type=type_restriction,
        motif=motif,
        fin=timezone.now() + timedelta(days=duree_jours),
        appliquee_par=acteur,
    )
    if type_restriction == Restriction.Type.COMPTE:
        client.est_bloque = True
        client.is_active = False
        client.save(update_fields=["est_bloque", "is_active"])
    audit = journaliser(acteur, "RESTRICTION_APPLIQUEE", restriction, {"fin": restriction.fin.isoformat(), "type": type_restriction})
    notifier(client, "Restriction appliquée", f"{restriction.get_type_display()} jusqu'au {restriction.fin:%d/%m/%Y}. Motif : {motif}", "SECURITY", journal_audit=audit)
    return restriction
