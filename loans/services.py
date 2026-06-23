from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import connection, transaction
from django.utils import timezone
from accounts.models import ConfigurationBibliotheque
from catalog.models import Livre
from reservations.models import Reservation
from .models import Emprunt
from .signals import emprunt_cree, retour_valide
from .validators import valider_poids, valider_qr


@transaction.atomic
def creer_emprunt(reservation_id, code_qr, bibliothecaire):
    """Convertit une réservation valide en emprunt et diminue le stock une seule fois."""
    from audit.services import journaliser
    from alerts.services import notifier

    reservation = Reservation.objects.select_for_update().select_related("client", "livre").get(pk=reservation_id)
    livre = Livre.objects.select_for_update().get(pk=reservation.livre_id)
    if reservation.statut != Reservation.Statut.ACTIVE or reservation.expire_le <= timezone.now():
        raise ValidationError("Cette réservation n'est plus active.")
    valider_qr(livre, code_qr)
    if livre.stock_disponible < 1:
        raise ValidationError("Aucun exemplaire physique n'est disponible.")
    configuration = ConfigurationBibliotheque.charger()
    if Emprunt.objects.actifs().filter(client=reservation.client).count() >= configuration.livres_max_par_client:
        raise ValidationError(f"Ce client a atteint la limite de {configuration.livres_max_par_client} emprunts actifs.")
    debut = timezone.localdate()
    emprunt = Emprunt.objects.create(
        client=reservation.client,
        livre=livre,
        reservation=reservation,
        valide_par=bibliothecaire,
        emprunte_le=debut,
        retour_prevu_le=debut + timedelta(days=configuration.duree_pret_jours),
    )
    # MySQL garantit la décrémentation par trigger ; SQLite garde ce repli pour les tests locaux.
    if connection.vendor == "mysql":
        livre.refresh_from_db(fields=["stock_disponible", "statut", "modifie_le"])
    else:
        livre.stock_disponible -= 1
        livre.save(update_fields=["stock_disponible", "modifie_le"])
    reservation.statut = Reservation.Statut.CONVERTIE
    reservation.verrou_actif = None
    reservation.save(update_fields=["statut", "verrou_actif"])
    livre.actualiser_statut()
    audit = journaliser(bibliothecaire, "EMPRUNT_CREE", emprunt, {"reservation_id": reservation.id, "retour_prevu": str(emprunt.retour_prevu_le)})
    notifier(emprunt.client, "Emprunt validé", f"{livre.titre} doit être rendu avant le {emprunt.retour_prevu_le:%d/%m/%Y}.", "LOAN", "/emprunts/historique/", journal_audit=audit)
    emprunt_cree.send(sender=Emprunt, emprunt=emprunt)
    return emprunt


@transaction.atomic
def enregistrer_retour(emprunt_id, code_qr, poids_mesure, etat, commentaire, bibliothecaire):
    """Clôture un retour après QR, pesée et inspection, puis applique les conséquences."""
    from abuse.services import creer_rapport_abus, evaluer_niveau_risque
    from audit.services import journaliser
    from alerts.services import notifier
    from penalties.services import creer_penalite

    emprunt = Emprunt.objects.select_for_update().select_related("client", "livre").get(pk=emprunt_id)
    livre = Livre.objects.select_for_update().get(pk=emprunt.livre_id)
    if emprunt.statut != Emprunt.Statut.EN_COURS:
        raise ValidationError("Cet emprunt est déjà clôturé ou en inspection.")
    valider_qr(livre, code_qr)
    poids_conforme = valider_poids(livre, poids_mesure)
    emprunt.poids_retour_grammes = poids_mesure
    emprunt.etat_retour = etat
    emprunt.commentaire_retour = commentaire

    # Un écart de poids impose une inspection même si l'état visuel semble correct.
    if not poids_conforme:
        emprunt.statut = Emprunt.Statut.INSPECTION
        emprunt.save(update_fields=["poids_retour_grammes", "etat_retour", "commentaire_retour", "statut"])
        creer_rapport_abus(emprunt.client, "ANOMALIE_POIDS", f"Écart de poids détecté pour {livre.titre}.", source=emprunt, severite="HIGH")
        audit = journaliser(bibliothecaire, "RETOUR_EN_INSPECTION", emprunt, {"poids": poids_mesure, "reference": livre.poids_reference_grammes})
        notifier(emprunt.client, "Retour en inspection", f"Le retour de {livre.titre} nécessite une inspection complémentaire.", "RETURN", journal_audit=audit)
        return emprunt

    emprunt.retourne_le = timezone.localdate()
    emprunt.statut = Emprunt.Statut.RETOURNE
    emprunt.save(update_fields=["poids_retour_grammes", "etat_retour", "commentaire_retour", "retourne_le", "statut"])
    if connection.vendor == "mysql":
        livre.refresh_from_db(fields=["stock_disponible", "statut", "modifie_le"])
    else:
        livre.stock_disponible = min(livre.stock_total, livre.stock_disponible + 1)
    if etat != Emprunt.EtatRetour.BON:
        livre.statut = Livre.Statut.MAINTENANCE
    livre.save(update_fields=["stock_disponible", "statut", "modifie_le"])
    if etat == Emprunt.EtatRetour.BON:
        livre.actualiser_statut()

    configuration = ConfigurationBibliotheque.charger()
    jours_factures = max(0, emprunt.jours_retard - configuration.delai_grace_jours)
    if jours_factures:
        creer_penalite(
            client=emprunt.client,
            emprunt=emprunt,
            type_penalite="LATE",
            montant=Decimal(jours_factures) * configuration.penalite_par_jour,
            motif=f"Retour avec {emprunt.jours_retard} jour(s) de retard, dont {jours_factures} facturé(s).",
            acteur=bibliothecaire,
        )
    if etat == Emprunt.EtatRetour.ENDOMMAGE:
        creer_penalite(emprunt.client, emprunt, "DAMAGE", configuration.penalite_dommage, "Ouvrage retourné endommagé.", bibliothecaire)
        creer_rapport_abus(emprunt.client, "LIVRE_ENDOMMAGE", commentaire or "Ouvrage endommagé.", source=emprunt, severite="HIGH")
    elif etat == Emprunt.EtatRetour.PERDU:
        creer_penalite(emprunt.client, emprunt, "LOSS", configuration.penalite_perte, "Ouvrage déclaré perdu.", bibliothecaire)
        creer_rapport_abus(emprunt.client, "LIVRE_PERDU", commentaire or "Ouvrage perdu.", source=emprunt, severite="CRITICAL")

    evaluer_niveau_risque(emprunt.client)
    audit = journaliser(bibliothecaire, "RETOUR_VALIDE", emprunt, {"retard": emprunt.jours_retard, "etat": etat, "poids_conforme": poids_conforme})
    notifier(emprunt.client, "Retour enregistré", f"Le retour de {livre.titre} a été validé.", "RETURN", "/emprunts/historique/", journal_audit=audit)
    retour_valide.send(sender=Emprunt, emprunt=emprunt)
    return emprunt
