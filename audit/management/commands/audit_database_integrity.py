from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.models import Count, F, Q
from catalog.models import Livre
from loans.models import Emprunt
from penalties.models import Penalite
from reservations.models import Reservation


class Command(BaseCommand):
    help = "Vérifie les garanties relationnelles et triggers de la base MySQL."

    triggers_attendus = {
        "smart_reservation_integrite_bi",
        "smart_reservation_identite_bu",
        "smart_reservation_statut_ai",
        "smart_reservation_statut_au",
        "smart_reservation_statut_ad",
        "smart_emprunt_stock_bi",
        "smart_emprunt_identite_bu",
        "smart_emprunt_stock_au",
        "smart_emprunt_historique_bd",
        "smart_penalite_integrite_bi",
        "smart_penalite_integrite_bu",
    }

    def handle(self, *args, **options):
        erreurs = []
        if connection.vendor != "mysql":
            raise CommandError("Cette vérification finale doit être exécutée sur MySQL.")

        with connection.cursor() as curseur:
            curseur.execute("SHOW TRIGGERS")
            presents = {ligne[0] for ligne in curseur.fetchall()}
        manquants = self.triggers_attendus - presents
        if manquants:
            erreurs.append(f"Triggers manquants : {', '.join(sorted(manquants))}")

        doublons = Reservation.objects.filter(statut=Reservation.Statut.ACTIVE).values("client_id", "livre_id").annotate(total=Count("id")).filter(total__gt=1)
        if doublons.exists():
            erreurs.append("Des réservations actives dupliquées existent.")

        penalites_incoherentes = Penalite.objects.filter(emprunt__isnull=False).exclude(client_id=F("emprunt__client_id"))
        if penalites_incoherentes.exists():
            erreurs.append("Une pénalité référence l'emprunt d'un autre client.")

        for livre in Livre.objects.all():
            occupes = Emprunt.objects.filter(livre=livre, statut__in=[Emprunt.Statut.EN_COURS, Emprunt.Statut.INSPECTION]).count()
            attendu = max(0, livre.stock_total - occupes)
            if livre.stock_disponible != attendu:
                erreurs.append(f"Stock incohérent pour {livre.titre}: {livre.stock_disponible} au lieu de {attendu}.")

        if erreurs:
            raise CommandError("\n".join(erreurs))
        self.stdout.write(self.style.SUCCESS(
            f"Intégrité MySQL validée : {len(presents & self.triggers_attendus)} triggers, stocks et relations cohérents."
        ))

