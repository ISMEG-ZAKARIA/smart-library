from datetime import timedelta
from decimal import Decimal
from pathlib import Path
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import ConfigurationBibliotheque, Utilisateur
from abuse.models import RapportAbus
from audit.models import JournalAudit
from catalog.models import Auteur, Categorie, Livre
from catalog.catalogue_data import CATALOGUE_DEMO
from loans.models import Emprunt
from penalties.models import Penalite
from reservations.models import Reservation


class Command(BaseCommand):
    help = "Crée un jeu de démonstration cohérent et idempotent pour la soutenance."

    def handle(self, *args, **options):
        ConfigurationBibliotheque.charger()
        admin, _ = Utilisateur.objects.get_or_create(
            email="admin@smartlibrary.local",
            defaults={"username": "admin", "cin": "AA100001", "first_name": "Yassine", "last_name": "El Fassi", "role": Utilisateur.Role.ADMIN, "is_staff": True, "is_superuser": True},
        )
        admin.set_password("AdminSmart2026!")
        admin.save()
        bibliothecaire, _ = Utilisateur.objects.get_or_create(
            email="bibliothecaire@smartlibrary.local",
            defaults={"username": "bibliothecaire", "cin": "BB100002", "first_name": "Nadia", "last_name": "Alaoui", "role": Utilisateur.Role.LIBRARIAN, "is_staff": True},
        )
        bibliothecaire.set_password("BiblioSmart2026!")
        bibliothecaire.save()
        client, _ = Utilisateur.objects.get_or_create(
            email="client@smartlibrary.local",
            defaults={"username": "client", "cin": "CC100003", "first_name": "Sofia", "last_name": "El Mansouri", "role": Utilisateur.Role.CLIENT},
        )
        client.set_password("ClientSmart2026!")
        client.save()
        risque, _ = Utilisateur.objects.get_or_create(
            email="ayoub@smartlibrary.local",
            defaults={"username": "ayoub", "cin": "DD100004", "first_name": "Ayoub", "last_name": "El Idrissi", "role": Utilisateur.Role.CLIENT, "score_risque": 70, "niveau_alerte": 2},
        )
        risque.set_password("ClientSmart2026!")
        risque.save()

        source_couvertures = Path(settings.BASE_DIR) / "assets" / "book_covers"
        destination_couvertures = Path(settings.MEDIA_ROOT) / "couvertures"
        destination_couvertures.mkdir(parents=True, exist_ok=True)

        livres_importes = {}
        for element in CATALOGUE_DEMO:
            source = source_couvertures / element["couverture"]
            destination = destination_couvertures / element["couverture"]
            if not source.exists():
                raise FileNotFoundError(f"Couverture introuvable : {source}")
            shutil.copy2(source, destination)

            categorie, _ = Categorie.objects.get_or_create(nom=element["categorie"])
            auteur, _ = Auteur.objects.get_or_create(nom=element["auteur"])
            livre, _ = Livre.objects.update_or_create(
                titre=element["titre"],
                defaults={
                    "isbn": element["isbn"],
                    "categorie": categorie,
                    "description": element["description"],
                    "annee_publication": element["annee"],
                    "editeur": element["editeur"],
                    "poids_reference_grammes": element["poids"],
                    "tolerance_poids_grammes": 15,
                    "couverture": f"couvertures/{element['couverture']}",
                    "visible_client": True,
                    "stock_total": element["stock"],
                    "stock_disponible": element["stock"],
                    "actif": True,
                },
            )
            livre.auteurs.set([auteur])
            livres_importes[element["titre"]] = livre

        livre = livres_importes["Le Petit Prince"]
        autre = livres_importes["1984"]

        Reservation.objects.get_or_create(client=client, livre=livre, statut=Reservation.Statut.ACTIVE, defaults={"expire_le": timezone.now() + timedelta(days=2)})
        emprunt, _ = Emprunt.objects.get_or_create(
            client=risque,
            livre=autre,
            statut=Emprunt.Statut.EN_COURS,
            defaults={"valide_par": bibliothecaire, "emprunte_le": timezone.localdate() - timedelta(days=35), "retour_prevu_le": timezone.localdate() - timedelta(days=20)},
        )
        for ouvrage in livres_importes.values():
            emprunts_actifs = Emprunt.objects.actifs().filter(livre=ouvrage).count()
            ouvrage.stock_disponible = max(0, ouvrage.stock_total - emprunts_actifs)
            ouvrage.save(update_fields=["stock_disponible", "modifie_le"])
            ouvrage.actualiser_statut()
        Penalite.objects.get_or_create(client=risque, emprunt=emprunt, type=Penalite.Type.RETARD, statut=Penalite.Statut.OUVERTE, defaults={"motif": "Retard critique supérieur à 15 jours.", "montant": Decimal("45.50"), "creee_par": bibliothecaire})
        RapportAbus.objects.get_or_create(client=risque, type_alerte="RETARD_CRITIQUE", statut=RapportAbus.Statut.OUVERT, defaults={"severite": RapportAbus.Severite.ELEVEE, "description": "Retard répété sur un ouvrage réservé."})
        JournalAudit.objects.get_or_create(action="DONNEES_DEMO_CHARGEES", cible_type="accounts.Utilisateur", cible_id=str(admin.pk), defaults={"acteur": admin, "description_cible": "Jeu de démonstration Smart Library"})

        self.stdout.write(self.style.SUCCESS("Données de démonstration prêtes : 12 livres illustrés importés."))
        self.stdout.write("Catalogue client : les 12 livres actifs sont visibles selon les permissions du client.")
        self.stdout.write("Admin: admin@smartlibrary.local / AdminSmart2026!")
        self.stdout.write("Bibliothécaire: bibliothecaire@smartlibrary.local / BiblioSmart2026!")
        self.stdout.write("Client: client@smartlibrary.local / ClientSmart2026!")
