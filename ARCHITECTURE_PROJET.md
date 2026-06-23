# Architecture du projet

Smart Library suit Django MVT. Les vues orchestrent l'entrée HTTP ; les formulaires valident les données ; les services portent les transactions métier ; les modèles garantissent le schéma ; les templates n'affichent que des données préparées.

## Racine

- `manage.py` : amorce la base MySQL avant les commandes qui en dépendent, puis lance Django.
- `requirements.txt` : dépendances Python reproductibles.
- `smart_library/settings.py` : applications, MySQL, authentification, fichiers statiques et langue.
- `smart_library/database.py` : création idempotente de `PFA_3IIR`.
- `smart_library/urls.py` : assemblage des routes des huit applications.
- `sql/create_database.sql` : solution SQL manuelle équivalente.
- `static/` : feuille de style, JavaScript léger, logo et couvertures.
- `templates/base/` : shell commun et formulaire générique.
- `templates/admin_interface/`, `client_interface/`, `librarian_interface/` : espaces visuels séparés.
- `tests/test_workflows.py` : tests d'intégration du cycle métier complet.

## Applications

### `accounts`

Responsable de `Utilisateur`, des rôles proxy, de `ConfigurationBibliotheque`, de la connexion, de l'inscription, du profil, des tableaux de bord, des utilisateurs et des paramètres. `permissions.py` contient le décorateur central de contrôle d'accès. `seed_demo` prépare une soutenance reproductible.

### `books`

Contient `Livre`, `Auteur`, `Categorie` et `Commentaire`. `Livre.actualiser_statut` synchronise stock, réservations et disponibilité. Le service d'enregistrement journalise les modifications de catalogue.

`books/catalogue_data.py` décrit les 12 ouvrages illustrés fournis. Les images originales sont conservées dans `assets/book_covers`, puis la commande `seed_demo` les copie dans `media/couvertures`. Le champ `Livre.visible_client` maintient une sélection de 4 titres côté client, sans limiter les catalogues administrateur et bibliothécaire.

### `reservations`

Contrôle les réservations actives, annulations et expirations. `services.py` verrouille les livres, vérifie quota/restrictions/stock et déclenche notification, audit et risque. La commande `expire_reservations` est prévue pour une tâche planifiée.

### `loans`

Porte `Emprunt`, la conversion d'une réservation, la diminution du stock et le retour hybride QR + poids + inspection. `managers.py` expose les emprunts actifs et en retard.

### `penalties`

Crée et règle les sanctions. Une création met à jour le compteur utilisateur, le risque, la notification et l'audit.

### `notifications`

Centralise les messages internes et l'envoi e-mail. Le context processor alimente le badge global des non-lues.

### `audit`

Conserve les traces sensibles. Le Django Admin interdit l'ajout et la modification manuels afin de protéger la valeur probante du journal.

### `abuse`

Centralise `RapportAbus`, `Restriction` et le score de risque. Les restrictions sont consultées directement par le validateur de réservation.

### `stats`

`stats/services.py` est l'unique couche d'agrégation des dashboards. Il calcule les statistiques globales, opérationnelles, par client, livre, pénalité, emprunt et réservation avec l'ORM. Cette application ne possède aucune table ni cache métier.

## Synchronisation globale

- Source unique de vérité : MySQL `PFA_3IIR` et les modèles Django partagés par les rôles.
- Stock : triggers `smart_emprunt_stock_bi` et `smart_emprunt_stock_au` créés par migrations.
- Disponibilité : triggers `smart_reservation_statut_*` recalculant `Livre.statut`.
- Notifications : `notifications/services.py::notifier`, avec FK obligatoire vers `JournalAudit` pour les événements métier.
- Audit : `audit/services.py::journaliser`, acteur et cible persistés.
- Rôles : vues globales pour Admin/Bibliothécaire, filtres `client=request.user` pour le Client.
- Contrôle : `python manage.py audit_database_integrity` interroge directement MySQL.

## Interactions

```text
Vue HTTP -> Formulaire/permission -> Service transactionnel
         -> Modèles verrouillés
         -> Notification + Audit + Risque
         -> Template du rôle
```

Les imports entre applications sont placés dans les fonctions de service lorsque cela évite les cycles Python. Les relations de base restent exprimées par des clés étrangères et des migrations Django.

## Sécurité et cohérence

- CSRF sur chaque action POST ;
- authentification Django et mots de passe hachés ;
- contrôle de rôle centralisé ;
- `transaction.atomic` sur les workflows multi-modules ;
- `select_for_update` sur livre, réservation, emprunt et pénalité sensibles ;
- contraintes de stock en base ;
- suppression protégée pour l'historique d'emprunt ;
- SQL MySQL en mode strict et encodage `utf8mb4`.
