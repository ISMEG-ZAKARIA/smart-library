import uuid
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Count, Q
from .validators import valider_isbn


class Auteur(models.Model):
    nom = models.CharField(max_length=120)
    biographie = models.TextField(blank=True)

    class Meta:
        ordering = ["nom"]
        constraints = [models.UniqueConstraint(fields=["nom"], name="auteur_nom_unique")]

    def __str__(self):
        return self.nom


class Categorie(models.Model):
    nom = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class LivreQuerySet(models.QuerySet):
    def disponibles(self):
        return self.annotate(
            reservations_actives=Count("reservations", filter=Q(reservations__statut="ACTIVE"))
        ).filter(stock_disponible__gt=models.F("reservations_actives"), actif=True)


class Livre(models.Model):
    class Statut(models.TextChoices):
        DISPONIBLE = "AVAILABLE", "Disponible"
        RESERVE = "RESERVED", "Réservé"
        INDISPONIBLE = "UNAVAILABLE", "Indisponible"
        MAINTENANCE = "MAINTENANCE", "En maintenance"

    titre = models.CharField(max_length=220, db_index=True)
    isbn = models.CharField(max_length=17, unique=True, validators=[valider_isbn])
    auteurs = models.ManyToManyField(Auteur, related_name="livres")
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="livres")
    description = models.TextField()
    annee_publication = models.PositiveSmallIntegerField(null=True, blank=True)
    editeur = models.CharField(max_length=150, blank=True)
    poids_reference_grammes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    tolerance_poids_grammes = models.PositiveSmallIntegerField(default=15)
    code_qr = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    couverture = models.ImageField(upload_to="couvertures/", blank=True)
    visible_client = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Visible dans le catalogue client par défaut ; décochez uniquement pour un ouvrage interne.",
    )
    stock_total = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    stock_disponible = models.PositiveIntegerField(default=1)
    statut = models.CharField(max_length=15, choices=Statut.choices, default=Statut.DISPONIBLE, db_index=True)
    actif = models.BooleanField(default=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    objects = LivreQuerySet.as_manager()

    class Meta:
        ordering = ["titre"]
        constraints = [
            models.CheckConstraint(condition=Q(stock_total__gte=1), name="livre_stock_total_positif"),
            models.CheckConstraint(condition=Q(stock_disponible__gte=0), name="livre_stock_disponible_positif"),
            models.CheckConstraint(condition=Q(stock_disponible__lte=models.F("stock_total")), name="livre_stock_disponible_valide"),
        ]

    def __str__(self):
        return self.titre

    def actualiser_statut(self):
        """Synchronise le statut avec le stock physique et les réservations actives."""
        from django.utils import timezone

        if not self.actif or self.statut == self.Statut.MAINTENANCE:
            nouveau = self.Statut.INDISPONIBLE if not self.actif else self.Statut.MAINTENANCE
        elif self.stock_disponible == 0:
            nouveau = self.Statut.INDISPONIBLE
        else:
            actives = self.reservations.filter(statut="ACTIVE", expire_le__gt=timezone.now()).count()
            nouveau = self.Statut.RESERVE if actives >= self.stock_disponible else self.Statut.DISPONIBLE
        if self.statut != nouveau:
            self.statut = nouveau
            self.save(update_fields=["statut", "modifie_le"])
        return nouveau


class Commentaire(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="commentaires")
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name="commentaires")
    note = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    texte = models.TextField(max_length=1500)
    cree_le = models.DateTimeField(auto_now_add=True)
    modere = models.BooleanField(default=False)

    class Meta:
        ordering = ["-cree_le"]
        constraints = [models.UniqueConstraint(fields=["client", "livre"], name="avis_unique_par_client_livre")]

    def __str__(self):
        return f"{self.client} — {self.livre}"
