# Guide de soutenance

## Où est implémentée la réservation ?

- modèle : `reservations/models.py::Reservation` ;
- règles et synchronisation : `reservations/services.py::creer_reservation` ;
- contrôle du client : `reservations/validators.py` ;
- vues : `reservations/views.py` ;
- écran : `templates/reservations/liste.html` ;
- preuve automatisée : `WorkflowMetierTests.test_reservation_synchronise_catalogue_notification_audit`.

## Où est calculée la pénalité ?

Le retard et le délai de grâce sont calculés dans `loans/services.py::enregistrer_retour`. La création, la notification, l'audit et le recalcul du risque sont dans `penalties/services.py::creer_penalite`. Le tarif vient de `ConfigurationBibliotheque.penalite_par_jour`.

## Où est gérée la détection d'abus ?

Les modèles et le score se trouvent dans `abuse/models.py` et `abuse/services.py`. Les workflows métier appellent `creer_rapport_abus` au moment exact d'une expiration, d'un écart de poids, d'un dommage ou d'une perte. L'écran administrateur est `templates/admin_interface/abus.html`.

## Où est gérée l'authentification ?

`AUTH_USER_MODEL = accounts.Utilisateur` dans `settings.py`. Les vues et formulaires sont dans `accounts/views.py` et `accounts/forms.py`. Les autorisations sont centralisées dans `accounts/permissions.py::roles_requis`.

## Où sont les cardinalités UML ?

Dans les champs `ForeignKey`, `OneToOneField` et `ManyToManyField` des fichiers `models.py`. La justification relation par relation est dans `UML_MAPPING.md`.

## Où sont les règles métier ?

Dans les fichiers `services.py`, jamais dans les templates. `BUSINESS_RULES_MAPPING.md` associe chaque règle à sa fonction. Les validateurs isolent les contrôles réutilisables et les managers les requêtes de domaine.

## Comment prouvez-vous la synchronisation ?

Exemple retour : une seule fonction transactionnelle ferme l'emprunt, restitue le stock, calcule le retard, crée la pénalité, ouvre l'abus éventuel, recalcule le risque, notifie et audite. Si une étape échoue, Django annule toute la transaction.

La preuve structurelle se trouve dans les migrations `reservations/0002-0004`, `loans/0002-0004`, `penalties/0002-0003` et `notifications/0002-0003`. La commande `python manage.py audit_database_integrity` vérifie directement les 11 triggers et la cohérence des lignes MySQL.

## Où sont calculées les statistiques ?

Uniquement dans `stats/services.py`. Les trois dashboards appellent ce service et ne possèdent aucun chiffre stocké en dur. Pour la démonstration, créer une pénalité puis rafraîchir successivement les trois rôles : les compteurs proviennent immédiatement de la même ligne `Penalite`.

## Comment évitez-vous un double emprunt ?

La réservation et le livre sont verrouillés avec `select_for_update`, le statut actif est contrôlé, `reservation` est un `OneToOneField`, puis la réservation passe à `CONVERTED` dans la même transaction.

## Comment lance-t-on la démonstration ?

1. démarrer MySQL ;
2. `python -m pip install -r requirements.txt` ;
3. `python manage.py migrate` ;
4. `python manage.py seed_demo` ;
5. `python manage.py runserver` ;
6. ouvrir `http://127.0.0.1:8000/` avec l'un des comptes du `README.md`.

## Quels tests montrer ?

`tests/test_workflows.py` couvre la réservation synchronisée, la conversion en emprunt, le retour tardif avec pénalité, l'anomalie de poids, les restrictions, les permissions et le rendu des pages principales.
