"""Agrégations calculées exclusivement depuis les tables métier MySQL."""
from datetime import date
from django.db.models import Count, F, Q, Sum
from accounts.models import Utilisateur
from abuse.models import RapportAbus, Restriction
from audit.models import JournalAudit
from catalog.models import Livre
from loans.models import Emprunt
from alerts.models import Notification
from penalties.models import Penalite
from reservations.models import Reservation


def statistiques_admin():
    """Retourne l'état global instantané de la base pour les écrans administrateur."""
    retours = Emprunt.objects.filter(statut=Emprunt.Statut.RETOURNE)
    retours_total = retours.count()
    retours_retard = retours.filter(retourne_le__gt=F("retour_prevu_le")).count()
    reservations_total = Reservation.objects.count()
    reservations_converties = Reservation.objects.filter(statut=Reservation.Statut.CONVERTIE).count()
    return {
        "utilisateurs_actifs": Utilisateur.objects.filter(is_active=True, est_bloque=False).count(),
        "clients_bloques": Utilisateur.objects.filter(role=Utilisateur.Role.CLIENT, est_bloque=True).count(),
        "total_livres": Livre.objects.filter(actif=True).count(),
        "livres_disponibles": Livre.objects.filter(actif=True, stock_disponible__gt=0).count(),
        "livres_indisponibles": Livre.objects.filter(Q(actif=False) | Q(stock_disponible=0)).count(),
        "livres_endommages": Emprunt.objects.filter(etat_retour=Emprunt.EtatRetour.ENDOMMAGE).count(),
        "reservations_en_attente": Reservation.objects.filter(statut=Reservation.Statut.ACTIVE).count(),
        "reservations_acceptees": reservations_converties,
        "reservations_refusees": Reservation.objects.filter(statut=Reservation.Statut.REFUSEE).count(),
        "reservations_annulees": Reservation.objects.filter(statut=Reservation.Statut.ANNULEE).count(),
        "reservations_expirees": Reservation.objects.filter(statut=Reservation.Statut.EXPIREE).count(),
        "emprunts_actifs": Emprunt.objects.filter(statut=Emprunt.Statut.EN_COURS).count(),
        "emprunts_termines": retours_total,
        "retours_retard": Emprunt.objects.en_retard().count(),
        "retours_rendus_en_retard": retours_retard,
        "retours_total": retours_total,
        "taux_retours_heure": round((retours_total - retours_retard) * 100 / retours_total) if retours_total else 0,
        "penalites_appliquees": Penalite.objects.count(),
        "penalites_reglees": Penalite.objects.filter(statut=Penalite.Statut.REGLEE).count(),
        "penalites_ouvertes": Penalite.objects.filter(statut=Penalite.Statut.OUVERTE).count(),
        "montant_penalites": Penalite.objects.aggregate(total=Sum("montant"))["total"] or 0,
        "montant_penalites_ouvertes": Penalite.objects.filter(statut=Penalite.Statut.OUVERTE).aggregate(total=Sum("montant"))["total"] or 0,
        "notifications_non_lues": Notification.objects.filter(lue_le__isnull=True).count(),
        "rapports_abus_ouverts": RapportAbus.objects.filter(statut=RapportAbus.Statut.OUVERT).count(),
        "restrictions_actives": Restriction.objects.filter(active=True).count(),
        "activites_recentes": JournalAudit.objects.select_related("acteur")[:10],
        "taux_reussite": round(reservations_converties * 100 / reservations_total, 1) if reservations_total else 0,
    }


def statistiques_bibliothecaire():
    """Expose les indicateurs opérationnels issus des mêmes tables que l'admin."""
    globales = statistiques_admin()
    return {
        "reservations_a_valider": globales["reservations_en_attente"],
        "reservations_refusees": globales["reservations_refusees"],
        "emprunts_actifs": globales["emprunts_actifs"],
        "emprunts_termines": globales["emprunts_termines"],
        "retours_retard": globales["retours_retard"],
        "penalites_ouvertes": globales["penalites_ouvertes"],
        "penalites_reglees": globales["penalites_reglees"],
        "montant_penalites_ouvertes": globales["montant_penalites_ouvertes"],
        "livres_disponibles": globales["livres_disponibles"],
        "notifications_non_lues": globales["notifications_non_lues"],
    }


def statistiques_client(client):
    """Filtre chaque agrégat par le propriétaire connecté."""
    emprunts = Emprunt.objects.filter(client=client)
    penalites = Penalite.objects.filter(client=client)
    reservations = Reservation.objects.filter(client=client)
    return {
        "reservations_actives": reservations.filter(statut=Reservation.Statut.ACTIVE).count(),
        "reservations_total": reservations.count(),
        "emprunts_actifs": emprunts.filter(statut=Emprunt.Statut.EN_COURS).count(),
        "emprunts_termines": emprunts.filter(statut=Emprunt.Statut.RETOURNE).count(),
        "retards": emprunts.filter(statut=Emprunt.Statut.EN_COURS, retour_prevu_le__lt=date.today()).count(),
        "penalites_total": penalites.count(),
        "penalites_ouvertes": penalites.filter(statut=Penalite.Statut.OUVERTE).count(),
        "montant_penalites_ouvertes": penalites.filter(statut=Penalite.Statut.OUVERTE).aggregate(total=Sum("montant"))["total"] or 0,
        "notifications_non_lues": Notification.objects.filter(utilisateur=client, lue_le__isnull=True).count(),
        "rapports_abus_ouverts": RapportAbus.objects.filter(client=client, statut=RapportAbus.Statut.OUVERT).count(),
    }


def tendances_emprunts(nombre_mois=6):
    """Calcule les volumes mensuels sans série statique stockée dans un template."""
    mois_courant = date.today().replace(day=1)
    tendances = []
    for decalage in range(nombre_mois - 1, -1, -1):
        index = mois_courant.year * 12 + mois_courant.month - 1 - decalage
        annee, mois_zero = divmod(index, 12)
        mois = mois_zero + 1
        tendances.append({
            "label": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"][mois - 1],
            "total": Emprunt.objects.filter(emprunte_le__year=annee, emprunte_le__month=mois).count(),
        })
    maximum = max([point["total"] for point in tendances] + [1])
    for point in tendances:
        point["pourcentage"] = max(4, round(point["total"] * 100 / maximum))
    return tendances


def statistiques_par_livre():
    return Livre.objects.annotate(
        total_emprunts=Count("emprunts"),
        emprunts_actifs=Count("emprunts", filter=Q(emprunts__statut=Emprunt.Statut.EN_COURS)),
        reservations_actives=Count("reservations", filter=Q(reservations__statut=Reservation.Statut.ACTIVE)),
    )


def repartition_penalites():
    return Penalite.objects.values("type", "statut").annotate(total=Count("id"), montant=Sum("montant")).order_by("type", "statut")


def repartition_emprunts():
    return Emprunt.objects.values("statut").annotate(total=Count("id")).order_by("statut")


def repartition_reservations():
    return Reservation.objects.values("statut").annotate(total=Count("id")).order_by("statut")
