from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from .managers import AdministrateurManager, BibliothecaireManager, ClientManager
from .validators import valider_cin


class Utilisateur(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrateur"
        LIBRARIAN = "LIBRARIAN", "Bibliothécaire"
        CLIENT = "CLIENT", "Client"

    email = models.EmailField("adresse e-mail", unique=True)
    cin = models.CharField("CIN", max_length=13, unique=True, validators=[valider_cin])
    telephone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=12, choices=Role.choices, default=Role.CLIENT, db_index=True)
    niveau_alerte = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0)])
    score_risque = models.PositiveSmallIntegerField(default=0)
    est_bloque = models.BooleanField(default=False, db_index=True)
    deux_facteurs_actif = models.BooleanField(default=False)
    notifications_email = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "cin"]

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        ordering = ["last_name", "first_name", "username"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(role__in=["ADMIN", "LIBRARIAN", "CLIENT"]),
                name="utilisateur_role_valide",
            ),
            models.CheckConstraint(condition=models.Q(score_risque__lte=100), name="utilisateur_risque_max_100"),
        ]

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def est_client(self):
        return self.role == self.Role.CLIENT

    @property
    def est_bibliothecaire(self):
        return self.role == self.Role.LIBRARIAN

    @property
    def est_administrateur(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def nombre_penalites(self):
        """Calcule le total depuis la table des pénalités, sans compteur dupliqué."""
        return self.penalites.exclude(statut="CANCELLED").count()


class Client(Utilisateur):
    objects = ClientManager()

    class Meta:
        proxy = True
        verbose_name = "client"

    def save(self, *args, **kwargs):
        self.role = self.Role.CLIENT
        return super().save(*args, **kwargs)


class Bibliothecaire(Utilisateur):
    objects = BibliothecaireManager()

    class Meta:
        proxy = True
        verbose_name = "bibliothécaire"

    def save(self, *args, **kwargs):
        self.role = self.Role.LIBRARIAN
        return super().save(*args, **kwargs)


class Administrateur(Utilisateur):
    objects = AdministrateurManager()

    class Meta:
        proxy = True
        verbose_name = "administrateur"

    def save(self, *args, **kwargs):
        self.role = self.Role.ADMIN
        self.is_staff = True
        return super().save(*args, **kwargs)


class ConfigurationBibliotheque(models.Model):
    """Règles métier modifiables depuis l'espace administrateur."""

    nom_etablissement = models.CharField(max_length=150, default="Smart Library EMSI")
    duree_pret_jours = models.PositiveSmallIntegerField(default=15)
    livres_max_par_client = models.PositiveSmallIntegerField(default=5)
    penalite_par_jour = models.DecimalField(max_digits=8, decimal_places=2, default=0.50)
    penalite_dommage = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    penalite_perte = models.DecimalField(max_digits=10, decimal_places=2, default=300.00)
    delai_grace_jours = models.PositiveSmallIntegerField(default=2)
    expiration_reservation_jours = models.PositiveSmallIntegerField(default=3)
    alertes_retard = models.BooleanField(default=True)
    resume_hebdomadaire = models.BooleanField(default=True)
    duree_session_minutes = models.PositiveIntegerField(default=60)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "configuration de la bibliothèque"
        constraints = [
            models.CheckConstraint(condition=models.Q(duree_pret_jours__gte=1), name="config_duree_pret_positive"),
            models.CheckConstraint(condition=models.Q(livres_max_par_client__gte=1), name="config_quota_livres_positif"),
            models.CheckConstraint(condition=models.Q(penalite_par_jour__gte=0), name="config_penalite_jour_positive"),
            models.CheckConstraint(condition=models.Q(penalite_dommage__gte=0), name="config_penalite_dommage_positive"),
            models.CheckConstraint(condition=models.Q(penalite_perte__gte=0), name="config_penalite_perte_positive"),
            models.CheckConstraint(condition=models.Q(expiration_reservation_jours__gte=1), name="config_expiration_positive"),
        ]

    @classmethod
    def charger(cls):
        configuration, _ = cls.objects.get_or_create(pk=1)
        return configuration

    def __str__(self):
        return self.nom_etablissement
