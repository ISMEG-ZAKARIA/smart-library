# Audit de synchronisation globale

Date de l'audit : 20 juin 2026. Base auditée : MySQL `PFA_3IIR`.

## État initial constaté

| Problème détecté | Fichier ou table | Cause | Correction structurelle prévue | Modules impactés | Validation prévue |
|---|---|---|---|---|---|
| Statistiques dispersées entre plusieurs vues | `accounts/views.py`, `abuse/views.py` | Agrégations ORM dupliquées, absence de service statistique unique | Créer `stats/services.py` et faire consommer ses résultats par les trois rôles | dashboards, pénalités, prêts, réservations, livres, abus | Tests croisés après chaque mutation |
| Stock protégé seulement par les services Python | `loans/services.py`, `books_livre` | Aucun trigger MySQL ; une insertion ORM directe peut contourner la décrémentation | Ajouter des triggers MySQL transactionnels et conserver un repli explicite pour SQLite | livres, emprunts, retours, statistiques | Insertion directe d'un emprunt puis lecture du stock |
| Réservations actives en double possibles en base | `reservations_reservation` | Le contrôle existe dans le service mais pas comme contrainte MySQL | Ajouter un verrou nullable et une contrainte unique `(client, livre, verrou_actif)` cohérente avec le statut | réservations, disponibilité, emprunts | Test de violation d'intégrité directe |
| Notification sans relation avec l'action auditée | `notifications_notification`, `audit_journalaudit` | Seul le destinataire est une clé étrangère ; la cause métier n'est pas liée | Ajouter `Notification.journal_audit` et produire audit puis notification dans la même transaction | notifications, audit, tous les services | Vérifier la FK pour chaque scénario critique |
| Contraintes métier insuffisantes | modèles `Reservation`, `Emprunt`, `Penalite`, `Restriction`, `Utilisateur` | Montants, dates, score, rôles et transitions reposent trop sur les formulaires | Ajouter `CheckConstraint`, `UniqueConstraint` et indexes par requête métier | tous les modules | Introspection MySQL + tests `IntegrityError` |
| Réservations invisibles pour l'administrateur | `reservations/views.py`, navigation | Seule la liste personnelle client et la file active bibliothécaire existent | Ajouter un suivi persistant filtré par rôle, sans dupliquer de table | admin, bibliothécaire, client | Même PK visible dans les vues autorisées |
| Emprunts terminés non consultables globalement | `loans/views.py` | La vue personnel ne montre que les retours actifs | Ajouter une vue de suivi global alimentée par `Emprunt` | admin, bibliothécaire, client | Même emprunt visible personnel/client |
| Livre désactivé sans workflow d'interface | `books/services.py`, `books/views.py` | Pas d'action de retrait synchronisée ni d'audit dédié | Ajouter une désactivation métier refusée si réservation/emprunt actif | catalogues et statistiques | Livre absent du client après désactivation |
| Modifications utilisateur insuffisamment auditées | `accounts/views.py` | Sauvegarde directe du formulaire | Centraliser la sauvegarde avec comparaison des champs et audit | comptes, rôles, audit | Audit contenant les champs modifiés |
| Montants dommage/perte codés dans le service | `loans/services.py` | Valeurs `100` et `300` non configurables | Déplacer les montants dans `ConfigurationBibliotheque` | retours, pénalités, paramètres, statistiques | Modification de règle puis nouveau retour |
| Données de démonstration mélangées aux garanties métier | `seed_demo` | Jeu initial nécessaire à la démo mais sans distinction documentaire | Conserver la commande uniquement comme amorçage ; toutes les pages continueront à interroger MySQL | démarrage et démonstration | Redémarrage serveur sans réexécuter la commande |

## Points déjà conformes avant correction

- Un seul modèle persistant existe pour chaque entité métier : `Livre`, `Reservation`, `Emprunt`, `Penalite`, `Notification`, `JournalAudit` et `RapportAbus`.
- Les interfaces de pénalités lisent déjà la même table `penalties_penalite`, avec filtre propriétaire pour le client.
- Les clés étrangères minimales Client → Réservation/Emprunt/Pénalité/Notification/Rapport d'abus sont présentes.
- `Emprunt.reservation` est un `OneToOneField` et `Livre.auteurs` un `ManyToManyField`.
- Les workflows critiques utilisent déjà `transaction.atomic()` et `select_for_update()`.

## Corrections appliquées

| Correction | Implémentation | Garantie obtenue | Test validé |
|---|---|---|---|
| Source unique des pénalités | Suppression du champ stocké `Utilisateur.nombre_penalites`; calcul depuis `Penalite` ou annotation `Count` | Aucun compteur utilisateur ne peut diverger de la table principale | `test_penalite_unique_visible_et_comptee_dans_les_trois_interfaces` |
| Statistiques centralisées | `stats/services.py` | Admin, bibliothécaire et client interrogent les mêmes modèles et filtres propriétaires | Assertions avant/après mutation dans 18 tests |
| Réservation active unique | `Reservation.verrou_actif`, `reservation_active_unique`, `reservation_verrou_coherent` | MySQL refuse un doublon même hors service | `test_mysql_refuse_reservation_active_dupliquee` |
| Stock piloté par MySQL | migrations `loans/0003` et `0004`, triggers `smart_emprunt_*` | Une insertion directe diminue le stock ; un retour le restitue ; l'historique d'emprunt ne peut être supprimé | `test_trigger_mysql_diminue_et_restitue_stock_sans_service` |
| Capacité de réservation pilotée par MySQL | migrations `reservations/0003` et `0004`, triggers `smart_reservation_*` | Rôle client, capacité et statut du livre contrôlés en base | contrainte directe + commande d'intégrité |
| Cohérence pénalité-emprunt-client | migration `penalties/0003_mysql_penalty_integrity.py` | MySQL rejette un emprunt appartenant à un autre client | `test_mysql_refuse_penalite_liee_a_emprunt_autre_client` |
| Notification reliée à l'audit | `Notification.journal_audit`, contrainte `notification_metier_auditee` | Toute notification non système pointe vers l'action persistée qui l'a produite | assertions FK réservation et pénalité |
| Visibilité inter-rôles | `reservations:suivi`, `loans:suivi`, listes de pénalités communes | Le personnel lit toutes les lignes autorisées ; le client lit seulement les siennes | tests de pages et de contenu croisé |
| Refus et annulation persistants | `refuser_reservation`, `annuler_penalite` | Aucune suppression d'historique ; décision, auteur, date, notification et audit conservés | `test_refus_reservation_persiste_notifie_audite_et_libere_livre` |
| Retrait synchronisé d'un livre | `books.services.desactiver_livre` | Le livre disparaît immédiatement des catalogues actifs et des statistiques sans casser ses FK historiques | `test_retrait_livre_est_immediat_dans_catalogue_et_statistiques` |
| Tarifs configurables | `ConfigurationBibliotheque.penalite_dommage`, `penalite_perte` | Aucun montant dommage/perte n'est codé dans le service de retour | migrations et formulaire Paramètres |

## Validation MySQL finale

- `python manage.py audit_database_integrity` : 11 triggers attendus présents, aucun doublon actif, aucune pénalité liée au mauvais client et stocks cohérents.
- `python manage.py test` : 18 tests réussis sur `test_PFA_3IIR`.
- La fermeture puis la réouverture des connexions serveur ne change aucun résultat, car les dashboards ne conservent aucun état en mémoire.

### Scénario manuel inter-rôles exécuté

Une pénalité marquée `SYNC-MYSQL-20260620` a été créée par POST authentifié dans l'interface Admin pour le client de démonstration. La même clé primaire `2` a été relue dans les pages Admin, Bibliothécaire et Client. La notification `11` pointait vers le journal d'audit `12`. Après annulation métier, les compteurs ouverts Admin/Bibliothécaire/Client sont tous revenus à `0`. Le serveur Django a ensuite été arrêté et redémarré : la page Client a relu la pénalité et son statut `CANCELLED` depuis MySQL avec une réponse HTTP 200.
