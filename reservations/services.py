from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from accounts.models import ConfigurationBibliotheque
from catalog.models import Livre
from .models import Reservation
from .signals import reservation_creee, reservation_expiree
from .validators import valider_client_reservable


@transaction.atomic
def creer_reservation(client, livre_id):
    """Réserve un exemplaire et synchronise catalogue, notification, audit et abus."""
    from abuse.services import evaluer_niveau_risque
    from audit.services import journaliser
    from alerts.services import notifier

    valider_client_reservable(client)
    # Libère en base les anciens verrous expirés avant de poser l'unicité active.
    expirer_reservations()
    configuration = ConfigurationBibliotheque.charger()
    livre = Livre.objects.select_for_update().get(pk=livre_id)
    if not livre.visible_client:
        raise ValidationError("Cet ouvrage n'est pas proposé dans le catalogue client actuel.")
    if Reservation.objects.filter(client=client, livre=livre, statut=Reservation.Statut.ACTIVE).exists():
        raise ValidationError("Vous avez déjà une réservation active pour cet ouvrage.")
    if Reservation.objects.actives().filter(client=client).count() >= configuration.livres_max_par_client:
        raise ValidationError(f"Vous avez atteint la limite de {configuration.livres_max_par_client} réservations actives.")
    actives_livre = Reservation.objects.actives().filter(livre=livre).count()
    if not livre.actif or livre.statut == Livre.Statut.MAINTENANCE or actives_livre >= livre.stock_disponible:
        raise ValidationError("Aucun exemplaire n'est actuellement réservable.")

    reservation = Reservation.objects.create(
        client=client,
        livre=livre,
        expire_le=timezone.now() + timedelta(days=configuration.expiration_reservation_jours),
    )
    livre.actualiser_statut()
    audit = journaliser(client, "RESERVATION_CREEE", reservation, {"livre_id": livre.id, "expire_le": reservation.expire_le.isoformat()})
    notifier(client, "Réservation confirmée", f"{livre.titre} est réservé jusqu'au {reservation.expire_le:%d/%m/%Y %H:%M}.", "RESERVATION", "/reservations/", journal_audit=audit)
    evaluer_niveau_risque(client)
    reservation_creee.send(sender=Reservation, reservation=reservation)
    return reservation


@transaction.atomic
def annuler_reservation(reservation, acteur, motif="Annulation demandée par le client"):
    """Annule une réservation active et libère immédiatement sa disponibilité."""
    from audit.services import journaliser
    from alerts.services import notifier

    reservation = Reservation.objects.select_for_update().select_related("livre", "client").get(pk=reservation.pk)
    if reservation.statut != Reservation.Statut.ACTIVE:
        raise ValidationError("Seule une réservation active peut être annulée.")
    reservation.statut = Reservation.Statut.ANNULEE
    reservation.verrou_actif = None
    reservation.annulee_le = timezone.now()
    reservation.motif_annulation = motif
    reservation.save(update_fields=["statut", "verrou_actif", "annulee_le", "motif_annulation"])
    reservation.livre.actualiser_statut()
    audit = journaliser(acteur, "RESERVATION_ANNULEE", reservation, {"motif": motif})
    notifier(reservation.client, "Réservation annulée", f"La réservation de {reservation.livre.titre} a été annulée.", "RESERVATION", journal_audit=audit)
    return reservation


@transaction.atomic
def refuser_reservation(reservation, acteur, motif):
    """Refuse une réservation active avec décision persistée, notification et audit liés."""
    from audit.services import journaliser
    from alerts.services import notifier

    reservation = Reservation.objects.select_for_update().select_related("livre", "client").get(pk=reservation.pk)
    if reservation.statut != Reservation.Statut.ACTIVE:
        raise ValidationError("Seule une réservation active peut être refusée.")
    reservation.statut = Reservation.Statut.REFUSEE
    reservation.verrou_actif = None
    reservation.traitee_par = acteur
    reservation.traitee_le = timezone.now()
    reservation.motif_refus = motif
    reservation.save(update_fields=["statut", "verrou_actif", "traitee_par", "traitee_le", "motif_refus"])
    reservation.livre.actualiser_statut()
    audit = journaliser(acteur, "RESERVATION_REFUSEE", reservation, {"motif": motif})
    notifier(reservation.client, "Réservation refusée", f"La réservation de {reservation.livre.titre} a été refusée : {motif}", "RESERVATION", "/reservations/", journal_audit=audit)
    return reservation


@transaction.atomic
def expirer_reservations():
    """Expire toutes les réservations dépassant leur délai et incrémente les alertes."""
    from abuse.services import creer_rapport_abus, evaluer_niveau_risque
    from audit.services import journaliser
    from alerts.services import notifier

    compteur = 0
    for reservation in Reservation.objects.a_expirer().select_related("client", "livre").select_for_update():
        reservation.statut = Reservation.Statut.EXPIREE
        reservation.verrou_actif = None
        reservation.save(update_fields=["statut", "verrou_actif"])
        reservation.client.niveau_alerte += 1
        reservation.client.save(update_fields=["niveau_alerte"])
        reservation.livre.actualiser_statut()
        audit = journaliser(None, "RESERVATION_EXPIREE", reservation)
        notifier(reservation.client, "Réservation expirée", f"Le délai de retrait de {reservation.livre.titre} est dépassé.", "RESERVATION", journal_audit=audit)
        creer_rapport_abus(reservation.client, "RESERVATION_EXPIREE", "Réservation non retirée dans le délai imparti.", source=reservation)
        evaluer_niveau_risque(reservation.client)
        reservation_expiree.send(sender=Reservation, reservation=reservation)
        compteur += 1
    return compteur
