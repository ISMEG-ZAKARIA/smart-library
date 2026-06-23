from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import DatabaseError, IntegrityError, connection, transaction
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from accounts.models import ConfigurationBibliotheque, Utilisateur
from abuse.models import RapportAbus, Restriction
from abuse.services import appliquer_restriction
from audit.models import JournalAudit
from catalog.models import Auteur, Categorie, Livre
from catalog.services import desactiver_livre
from loans.models import Emprunt
from loans.services import creer_emprunt, enregistrer_retour
from alerts.models import Notification
from penalties.models import Penalite
from penalties.services import creer_penalite
from reservations.models import Reservation
from reservations.services import creer_reservation, refuser_reservation
from dashboard.services import statistiques_admin, statistiques_bibliothecaire, statistiques_client


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class WorkflowMetierTests(TestCase):
    def setUp(self):
        self.configuration = ConfigurationBibliotheque.charger()
        self.client_user = Utilisateur.objects.create_user(
            username="client-test", email="client@test.local", cin="AA123456", password="TestPass2026!", role=Utilisateur.Role.CLIENT
        )
        self.bibliothecaire = Utilisateur.objects.create_user(
            username="biblio-test", email="biblio@test.local", cin="BB123456", password="TestPass2026!", role=Utilisateur.Role.LIBRARIAN
        )
        self.admin = Utilisateur.objects.create_superuser(
            username="admin-test", email="admin@test.local", cin="CC123456", password="TestPass2026!", role=Utilisateur.Role.ADMIN
        )
        categorie = Categorie.objects.create(nom="Roman")
        auteur = Auteur.objects.create(nom="George Orwell")
        self.livre = Livre.objects.create(
            titre="1984",
            isbn="9780451524935",
            categorie=categorie,
            description="Roman d'anticipation.",
            poids_reference_grammes=350,
            tolerance_poids_grammes=10,
            stock_total=2,
            stock_disponible=2,
            visible_client=True,
        )
        self.livre.auteurs.add(auteur)

    def test_reservation_synchronise_catalogue_notification_audit(self):
        reservation = creer_reservation(self.client_user, self.livre.pk)
        self.livre.refresh_from_db()
        self.assertEqual(reservation.statut, Reservation.Statut.ACTIVE)
        self.assertEqual(self.livre.statut, Livre.Statut.DISPONIBLE)
        self.assertTrue(Notification.objects.filter(utilisateur=self.client_user, type=Notification.Type.RESERVATION).exists())
        self.assertTrue(JournalAudit.objects.filter(action="RESERVATION_CREEE", cible_id=str(reservation.pk)).exists())
        notification = Notification.objects.get(utilisateur=self.client_user, type=Notification.Type.RESERVATION)
        self.assertIsNotNone(notification.journal_audit_id)

    def test_emprunt_convertit_reservation_et_diminue_stock(self):
        reservation = creer_reservation(self.client_user, self.livre.pk)
        emprunt = creer_emprunt(reservation.pk, str(self.livre.code_qr), self.bibliothecaire)
        reservation.refresh_from_db()
        self.livre.refresh_from_db()
        self.assertEqual(reservation.statut, Reservation.Statut.CONVERTIE)
        self.assertEqual(self.livre.stock_disponible, 1)
        self.assertEqual(emprunt.client, self.client_user)
        self.assertTrue(JournalAudit.objects.filter(action="EMPRUNT_CREE").exists())

    def test_retour_en_retard_genere_penalite_et_restitue_stock(self):
        reservation = creer_reservation(self.client_user, self.livre.pk)
        emprunt = creer_emprunt(reservation.pk, str(self.livre.code_qr), self.bibliothecaire)
        emprunt.emprunte_le = timezone.localdate() - timedelta(days=20)
        emprunt.retour_prevu_le = timezone.localdate() - timedelta(days=5)
        emprunt.save(update_fields=["emprunte_le", "retour_prevu_le"])
        retour = enregistrer_retour(emprunt.pk, str(self.livre.code_qr), 350, Emprunt.EtatRetour.BON, "Conforme", self.bibliothecaire)
        self.livre.refresh_from_db()
        self.assertEqual(retour.statut, Emprunt.Statut.RETOURNE)
        self.assertEqual(self.livre.stock_disponible, 2)
        penalite = Penalite.objects.get(client=self.client_user, type=Penalite.Type.RETARD)
        self.assertEqual(penalite.montant, Decimal("1.50"))
        self.assertTrue(JournalAudit.objects.filter(action="RETOUR_VALIDE").exists())

    def test_ecart_de_poids_place_le_retour_en_inspection(self):
        reservation = creer_reservation(self.client_user, self.livre.pk)
        emprunt = creer_emprunt(reservation.pk, str(self.livre.code_qr), self.bibliothecaire)
        retour = enregistrer_retour(emprunt.pk, str(self.livre.code_qr), 300, Emprunt.EtatRetour.BON, "Écart détecté", self.bibliothecaire)
        self.assertEqual(retour.statut, Emprunt.Statut.INSPECTION)
        self.assertTrue(RapportAbus.objects.filter(client=self.client_user, type_alerte="ANOMALIE_POIDS").exists())

    def test_restriction_emprunts_bloque_nouvelle_reservation(self):
        appliquer_restriction(self.client_user, Restriction.Type.EMPRUNTS, "Trois alertes", 30, self.admin)
        with self.assertRaises(ValidationError):
            creer_reservation(self.client_user, self.livre.pk)

    def test_permissions_interdisent_espace_admin_au_client(self):
        self.client.force_login(self.client_user)
        reponse = self.client.get(reverse("accounts:utilisateurs"))
        self.assertEqual(reponse.status_code, 403)

    def test_pages_principales_sont_rendues(self):
        self.client.force_login(self.client_user)
        self.assertEqual(self.client.get(reverse("accounts:accueil")).status_code, 200)
        self.assertEqual(self.client.get(reverse("catalog:catalogue")).status_code, 200)
        self.assertEqual(self.client.get(reverse("reservations:liste")).status_code, 200)

    def test_nouveau_design_reste_limite_aux_interfaces_client(self):
        self.client.force_login(self.client_user)
        pages_client = {
            "accounts:accueil": "client-dashboard-panel",
            "catalog:catalogue": "client-book-grid",
            "reservations:liste": "client-reservation-grid",
            "loans:historique": "client-loan-list",
            "alerts:liste": "client-risk-progress",
            "penalties:liste": "client-penalty-layout",
            "accounts:profil": "client-profile-hero",
            "accounts:client_parametres": "client-settings-form",
        }
        for route, classe in pages_client.items():
            reponse = self.client.get(reverse(route))
            self.assertEqual(reponse.status_code, 200)
            self.assertContains(reponse, "client-sidebar")
            self.assertContains(reponse, classe)

        self.client.force_login(self.admin)
        catalogue_admin = self.client.get(reverse("catalog:catalogue"))
        self.assertContains(catalogue_admin, 'class="book-grid"')
        self.assertNotContains(catalogue_admin, "client-book-grid")

    def test_client_ne_peut_pas_modifier_identite_enregistree_par_cin(self):
        self.client_user.first_name = "Identité"
        self.client_user.last_name = "Officielle"
        self.client_user.save(update_fields=["first_name", "last_name"])
        self.client.force_login(self.client_user)

        reponse = self.client.post(
            reverse("accounts:client_parametres"),
            {
                "first_name": "Prénom falsifié",
                "last_name": "Nom falsifié",
                "telephone": "+212600000000",
                "notifications_email": "on",
            },
        )
        self.assertRedirects(reponse, reverse("accounts:client_parametres"))
        self.client_user.refresh_from_db()
        self.assertEqual(self.client_user.first_name, "Identité")
        self.assertEqual(self.client_user.last_name, "Officielle")
        self.assertEqual(self.client_user.telephone, "+212600000000")

    def test_notifications_sont_accessibles_depuis_utilisateur_et_page_alertes(self):
        notification = Notification.objects.create(
            utilisateur=self.client_user,
            titre="Notification de contrôle",
            message="Vérification de la relation utilisateur-notifications.",
        )
        self.assertEqual(self.client_user.notifications.get(pk=notification.pk), notification)
        self.client.force_login(self.client_user)
        reponse = self.client.get(reverse("alerts:liste"))
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, notification.titre)
        self.assertEqual(
            reponse.context["nombre_notifications_non_lues"],
            Notification.objects.filter(utilisateur=self.client_user, lue_le__isnull=True).count(),
        )

    def test_pages_bibliothecaire_sont_rendues(self):
        self.client.force_login(self.bibliothecaire)
        for nom in ("accounts:accueil", "reservations:suivi", "loans:validations", "loans:retours", "loans:suivi", "penalties:liste"):
            self.assertEqual(self.client.get(reverse(nom)).status_code, 200)

    def test_pages_administrateur_sont_rendues(self):
        self.client.force_login(self.admin)
        for nom in ("accounts:accueil", "accounts:utilisateurs", "accounts:statistiques", "accounts:parametres", "reservations:suivi", "loans:suivi", "penalties:liste", "abuse:centre", "audit:journal"):
            self.assertEqual(self.client.get(reverse(nom)).status_code, 200)

    def test_catalogue_client_masque_les_livres_reserves_au_personnel(self):
        livre_interne = Livre.objects.create(
            titre="Ouvrage interne",
            isbn="9780062316097",
            categorie=self.livre.categorie,
            description="Ouvrage uniquement visible par le personnel.",
            poids_reference_grammes=300,
            stock_total=1,
            stock_disponible=1,
            visible_client=False,
        )
        livre_interne.auteurs.set(self.livre.auteurs.all())
        self.client.force_login(self.client_user)
        reponse_client = self.client.get(reverse("catalog:catalogue"))
        self.assertEqual(reponse_client.context["page_obj"].paginator.count, 1)
        self.client.force_login(self.bibliothecaire)
        reponse_personnel = self.client.get(reverse("catalog:catalogue"))
        self.assertEqual(reponse_personnel.context["page_obj"].paginator.count, 2)

    def test_penalite_unique_visible_et_comptee_dans_les_trois_interfaces(self):
        avant_admin = statistiques_admin()["penalites_appliquees"]
        penalite = creer_penalite(self.client_user, None, Penalite.Type.AUTRE, Decimal("25.00"), "Test de synchronisation jury", self.admin)
        self.assertEqual(statistiques_admin()["penalites_appliquees"], avant_admin + 1)
        self.assertEqual(statistiques_bibliothecaire()["penalites_ouvertes"], 1)
        self.assertEqual(statistiques_client(self.client_user)["penalites_ouvertes"], 1)
        notification = Notification.objects.get(utilisateur=self.client_user, journal_audit__action="PENALITE_CREEE")
        self.assertEqual(notification.journal_audit.cible_id, str(penalite.pk))

        for utilisateur in (self.admin, self.bibliothecaire, self.client_user):
            self.client.force_login(utilisateur)
            reponse = self.client.get(reverse("penalties:liste"))
            self.assertContains(reponse, "Test de synchronisation jury")

    def test_creation_penalite_admin_persiste_dans_historique_client_et_statistiques(self):
        """Le POST réel de l'interface Admin relit une seule pénalité depuis MySQL partout."""
        self.client.force_login(self.admin)
        formulaire = self.client.get(reverse("penalties:creer"))
        self.assertEqual(formulaire.status_code, 200)
        self.assertContains(formulaire, "penalty-simple-form")
        self.assertContains(formulaire, "penalty-field-row", count=2)
        self.assertQuerySetEqual(
            formulaire.context["form"].fields["client"].queryset,
            [self.client_user],
        )

        total_avant = statistiques_admin()["penalites_appliquees"]
        reponse = self.client.post(
            reverse("penalties:creer"),
            {
                "client": self.client_user.pk,
                "emprunt": "",
                "type": Penalite.Type.AUTRE,
                "motif": "Pénalité créée depuis le formulaire administrateur",
                "montant": "32.50",
            },
        )
        penalite = Penalite.objects.get(motif="Pénalité créée depuis le formulaire administrateur")
        self.assertRedirects(
            reponse,
            f"{reverse('penalties:liste')}#historique-penalites",
            fetch_redirect_response=False,
        )
        self.assertEqual(penalite.client, self.client_user)
        self.assertEqual(penalite.creee_par, self.admin)
        self.assertEqual(statistiques_admin()["penalites_appliquees"], total_avant + 1)

        self.assertContains(self.client.get(reverse("penalties:liste")), penalite.motif)
        self.assertContains(self.client.get(reverse("abuse:centre")), penalite.motif)
        self.client.force_login(self.client_user)
        self.assertContains(self.client.get(reverse("penalties:liste")), penalite.motif)
        self.assertEqual(statistiques_client(self.client_user)["penalites_ouvertes"], 1)
        self.assertTrue(Notification.objects.filter(utilisateur=self.client_user, journal_audit__cible_id=str(penalite.pk)).exists())

    def test_table_utilisateurs_utilise_des_cellules_actions_alignees(self):
        self.client.force_login(self.admin)
        reponse = self.client.get(reverse("accounts:utilisateurs"))
        self.assertContains(reponse, 'class="users-table"')
        self.assertContains(reponse, 'class="users-actions-cell"')
        self.assertContains(reponse, 'class="table-icon-button"')

    def test_reservation_unique_reliee_aux_trois_roles_et_aux_stats(self):
        reservation = creer_reservation(self.client_user, self.livre.pk)
        self.assertEqual(statistiques_admin()["reservations_en_attente"], 1)
        self.assertEqual(statistiques_bibliothecaire()["reservations_a_valider"], 1)
        self.assertEqual(statistiques_client(self.client_user)["reservations_actives"], 1)

        self.client.force_login(self.client_user)
        self.assertContains(self.client.get(reverse("reservations:liste")), self.livre.titre)
        for utilisateur in (self.bibliothecaire, self.admin):
            self.client.force_login(utilisateur)
            reponse = self.client.get(reverse("reservations:suivi"))
            self.assertContains(reponse, self.client_user.email)
            self.assertContains(reponse, self.livre.titre)
        self.assertTrue(Reservation.objects.filter(pk=reservation.pk).exists())

    def test_refus_reservation_persiste_notifie_audite_et_libere_livre(self):
        reservation = creer_reservation(self.client_user, self.livre.pk)
        refuser_reservation(reservation, self.bibliothecaire, "Quota pédagogique atteint")
        reservation.refresh_from_db()
        self.assertEqual(reservation.statut, Reservation.Statut.REFUSEE)
        self.assertIsNone(reservation.verrou_actif)
        self.assertEqual(statistiques_admin()["reservations_refusees"], 1)
        self.assertTrue(Notification.objects.filter(utilisateur=self.client_user, journal_audit__action="RESERVATION_REFUSEE").exists())

    def test_trigger_mysql_diminue_et_restitue_stock_sans_service(self):
        if connection.vendor != "mysql":
            self.skipTest("Garantie spécifique à MySQL")
        emprunt = Emprunt.objects.create(
            client=self.client_user,
            livre=self.livre,
            valide_par=self.bibliothecaire,
            emprunte_le=timezone.localdate(),
            retour_prevu_le=timezone.localdate() + timedelta(days=15),
        )
        self.livre.refresh_from_db()
        self.assertEqual(self.livre.stock_disponible, 1)
        emprunt.statut = Emprunt.Statut.RETOURNE
        emprunt.retourne_le = timezone.localdate()
        emprunt.save(update_fields=["statut", "retourne_le"])
        self.livre.refresh_from_db()
        self.assertEqual(self.livre.stock_disponible, 2)

    def test_mysql_refuse_reservation_active_dupliquee(self):
        creer_reservation(self.client_user, self.livre.pk)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Reservation.objects.create(
                client=self.client_user,
                livre=self.livre,
                expire_le=timezone.now() + timedelta(days=2),
            )

    def test_mysql_refuse_penalite_liee_a_emprunt_autre_client(self):
        autre_client = Utilisateur.objects.create_user(
            username="autre", email="autre@test.local", cin="DD123456", password="TestPass2026!", role=Utilisateur.Role.CLIENT
        )
        emprunt = Emprunt.objects.create(
            client=autre_client,
            livre=self.livre,
            valide_par=self.bibliothecaire,
            emprunte_le=timezone.localdate(),
            retour_prevu_le=timezone.localdate() + timedelta(days=15),
        )
        with self.assertRaises(DatabaseError), transaction.atomic():
            Penalite.objects.create(
                client=self.client_user,
                emprunt=emprunt,
                type=Penalite.Type.AUTRE,
                motif="Relation invalide",
                montant=Decimal("10.00"),
                creee_par=self.admin,
            )

    def test_retrait_livre_est_immediat_dans_catalogue_et_statistiques(self):
        total_avant = statistiques_admin()["total_livres"]
        desactiver_livre(self.livre.pk, self.admin, "Retrait de validation")
        self.assertEqual(statistiques_admin()["total_livres"], total_avant - 1)
        self.client.force_login(self.client_user)
        self.assertNotContains(self.client.get(reverse("catalog:catalogue")), self.livre.titre)
        self.assertTrue(JournalAudit.objects.filter(action="LIVRE_RETIRE", cible_id=str(self.livre.pk)).exists())


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class ImportCatalogueTests(TestCase):
    def test_commande_demo_importe_douze_couvertures_et_douze_livres_clients(self):
        call_command("seed_demo", verbosity=0)
        self.assertEqual(Livre.objects.count(), 12)
        self.assertEqual(Livre.objects.filter(visible_client=True).count(), 12)
        self.assertEqual(Livre.objects.exclude(couverture="").count(), 12)
