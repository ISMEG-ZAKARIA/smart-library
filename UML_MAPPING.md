# Correspondance UML → Django

## Classes

| Classe UML | Modèle Django | Fichier | Responsabilité métier |
|---|---|---|---|
| Utilisateur | `Utilisateur` | `accounts/models.py` | Compte authentifié, rôle, CIN, alertes, risque et blocage. |
| Client | `Client` | `accounts/models.py` | Vue proxy des utilisateurs ayant le rôle client. |
| Bibliothécaire | `Bibliothecaire` | `accounts/models.py` | Vue proxy du personnel chargé des opérations quotidiennes. |
| Administrateur | `Administrateur` | `accounts/models.py` | Vue proxy du personnel de supervision. |
| Livre | `Livre` | `books/models.py` | Ouvrage, couverture, QR, poids, stock, disponibilité et visibilité client. |
| Auteur | `Auteur` | `books/models.py` | Auteur lié à un ou plusieurs ouvrages. |
| Catégorie | `Categorie` | `books/models.py` | Classement thématique des ouvrages. |
| Réservation | `Reservation` | `reservations/models.py` | Demande limitée dans le temps avant un emprunt. |
| Emprunt | `Emprunt` | `loans/models.py` | Circulation physique d'un ouvrage et contrôle de son retour. |
| Pénalité | `Penalite` | `penalties/models.py` | Sanction financière issue d'un retard, dommage ou perte. |
| Commentaire | `Commentaire` | `books/models.py` | Avis unique d'un client sur un ouvrage. |
| Notification | `Notification` | `notifications/models.py` | Information interne reliée par FK à l'action du journal d'audit. |
| Journal | `JournalAudit` | `audit/models.py` | Trace immuable des opérations sensibles. |
| Rapport d'abus | `RapportAbus` | `abuse/models.py` | Anomalie comportementale issue d'un workflow métier. |
| Restriction | `Restriction` | `abuse/models.py` | Suspension temporaire ou blocage administratif. |
| Règles système | `ConfigurationBibliotheque` | `accounts/models.py` | Durées, quotas, grâce et tarif journalier. |

## Cardinalités

### Client (1) — (N) Réservation

`Reservation.client` est une `ForeignKey(..., related_name="reservations")`. Un client peut réserver plusieurs ouvrages ; chaque réservation appartient à un seul client.

### Livre (1) — (N) Réservation

`Reservation.livre` est une `ForeignKey(..., on_delete=PROTECT, related_name="reservations")`. Un livre peut être réservé plusieurs fois dans le temps ; une réservation vise un seul livre.

### Réservation (0..1) — (1) Emprunt

`Emprunt.reservation` est une `OneToOneField(..., null=True, related_name="emprunt")`. Une réservation produit au maximum un emprunt et un emprunt de comptoir peut exceptionnellement ne pas provenir d'une réservation.

### Client (1) — (N) Emprunt

`Emprunt.client` est une `ForeignKey(..., related_name="emprunts")`. Le client conserve tout son historique ; chaque emprunt a un seul titulaire.

### Livre (1) — (N) Emprunt

`Emprunt.livre` est une `ForeignKey(..., on_delete=PROTECT, related_name="emprunts")`. La suppression d'un ouvrage ayant circulé est interdite afin de préserver l'historique.

### Emprunt (1) — (N) Pénalité

`Penalite.emprunt` est une `ForeignKey(..., null=True, related_name="penalites")`. Un retour peut générer une pénalité de retard et une pénalité de dommage ; une sanction administrative peut ne pas être liée à un emprunt.

### Livre (N) — (N) Auteur

`Livre.auteurs` est une `ManyToManyField(Auteur, related_name="livres")`. Un ouvrage peut avoir plusieurs auteurs et un auteur plusieurs ouvrages.

### Catégorie (1) — (N) Livre

`Livre.categorie` est une `ForeignKey(..., on_delete=PROTECT, related_name="livres")`.

### Client (1) — (N) Commentaire et Livre (1) — (N) Commentaire

Les deux `ForeignKey` de `Commentaire` matérialisent l'association. La contrainte `avis_unique_par_client_livre` garantit au plus un avis par couple client/livre.

### Utilisateur (1) — (N) Notification / Journal / RapportAbus / Restriction

Les clés étrangères correspondantes se trouvent respectivement dans `notifications/models.py`, `audit/models.py` et `abuse/models.py`. Les acteurs d'audit sont conservés avec `SET_NULL`, tandis que les données personnelles appartenant au client utilisent `CASCADE` ou `PROTECT` selon les exigences de traçabilité.

### JournalAudit (1) — (N) Notification

`Notification.journal_audit` est une `ForeignKey(..., on_delete=PROTECT, related_name="notifications_generees")`. Une action auditée peut notifier plusieurs destinataires ; une notification métier ne peut exister sans sa preuve d'audit.
