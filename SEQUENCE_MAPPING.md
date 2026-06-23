# Traçabilité des diagrammes de séquence

## Inscription et authentification

- Vue : `accounts/views.py::inscription`, `ConnexionView`.
- Formulaires : `InscriptionForm`, `ConnexionForm`.
- Modèles : `Utilisateur`, `Notification`.
- Signal : `accounts.signals::notifier_creation_compte`.
- Déroulement : validation des données et du mot de passe, création du compte client, notification de bienvenue, authentification Django, puis redirection vers le tableau de bord du rôle.

## Réservation et emprunt par QR

- Vues : `reservations/views.py::creer`, `loans/views.py::valider`.
- Services : `creer_reservation`, `creer_emprunt`.
- Modèles : `Reservation`, `Livre`, `Emprunt`, `Notification`, `JournalAudit`, `RapportAbus`.
- Signaux : `reservation_creee`, `emprunt_cree`.
- Déroulement : contrôle du rôle, du blocage, des restrictions, du quota et du stock ; création de la réservation ; recalcul de disponibilité ; au comptoir, verrouillage de la réservation et du livre ; comparaison exacte du QR ; création de l'emprunt ; diminution du stock ; conversion de la réservation ; notification et audit.
- Exceptions : réservation expirée, mauvais QR, restriction active, quota atteint et stock nul produisent une erreur métier sans écriture partielle grâce à `transaction.atomic`.

## Retour avec vérification hybride

- Vue : `loans/views.py::retour`.
- Service : `loans/services.py::enregistrer_retour`.
- Modèles : `Emprunt`, `Livre`, `Penalite`, `RapportAbus`, `Notification`, `JournalAudit`.
- Signal : `retour_valide`.
- Déroulement : scan du QR, comparaison du poids avec la tolérance, inspection humaine, calcul du retard, restitution du stock, pénalité éventuelle, anomalie éventuelle, recalcul du risque, notification et audit.
- Exception de poids : le statut devient `INSPECTION`, un rapport d'abus est ouvert et le stock n'est pas restitué avant décision humaine.

## Expiration automatique

- Commande : `reservations/management/commands/expire_reservations.py`.
- Service : `expirer_reservations`.
- Signal : `reservation_expiree`.
- Déroulement : sélection verrouillée des réservations dépassées, statut expiré, disponibilité recalculée, alerte client incrémentée, rapport d'abus, notification, audit et recalcul du risque.

## Restriction administrative

- Vue : `abuse/views.py::centre`.
- Service : `appliquer_restriction`.
- Modèles : `Restriction`, `Utilisateur`, `Notification`, `JournalAudit`.
- Déroulement : validation du formulaire, création de la restriction datée, blocage éventuel du compte, notification et journalisation. Les validateurs de réservation consultent ensuite cette restriction.

## Synchronisation globale d'une pénalité

- Vue créatrice : `penalties/views.py::creer` pour Admin ou Bibliothécaire.
- Service : `penalties/services.py::creer_penalite`.
- Écriture unique : `penalties_penalite` avec FK `client`, `emprunt`, `creee_par`.
- Garantie MySQL : triggers `smart_penalite_integrite_bi/bu`.
- Lecture Admin/Bibliothécaire : `penalties/views.py::liste` sans filtre propriétaire.
- Lecture Client : même vue et même modèle, filtrés par `client=request.user`.
- Statistiques : `stats.services.statistiques_admin`, `statistiques_bibliothecaire`, `statistiques_client`.
- Effets : `JournalAudit`, puis `Notification.journal_audit` et recalcul de risque, dans la transaction.

## Synchronisation au niveau MySQL

Les migrations installent les triggers de réservation, emprunt et pénalité. Ils s'exécutent également lors d'une écriture ORM directe ou depuis Django Admin. Les services restent responsables des notifications, de l'audit et des règles nécessitant un acteur humain, tandis que MySQL protège les relations et le stock.
