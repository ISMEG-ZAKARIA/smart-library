# Traçabilité des règles métier

| Règle | Fichier et fonction | Explication |
|---|---|---|
| Une réservation expire après le délai configuré, trois jours par défaut. | `reservations/services.py::creer_reservation`, `expirer_reservations` | La date est calculée depuis `ConfigurationBibliotheque.expiration_reservation_jours`. |
| Un compte bloqué ne réserve pas. | `reservations/validators.py::valider_client_reservable` | Le service échoue avant toute écriture. |
| Une restriction d'emprunt bloque réservation et emprunt. | `reservations/validators.py::valider_client_reservable` | La restriction doit être active et non échue. |
| Le quota est vérifié à la réservation et à la remise. | `creer_reservation`, `loans/services.py::creer_emprunt` | La valeur provient de la configuration globale. |
| Un même client ne réserve pas deux fois le même livre activement. | `creer_reservation` | Contrôle effectué sous transaction. |
| Le stock disponible doit couvrir les réservations actives. | `creer_reservation`, `Livre.actualiser_statut` | Le statut devient réservé lorsque tous les exemplaires disponibles sont promis. |
| Le personnel voit les 12 livres, le client seulement 4. | `books/views.py::catalogue`, `Livre.visible_client`, `seed_demo` | La sélection client est pseudo-aléatoire mais reproductible pour stabiliser la démonstration. |
| Le QR doit correspondre au livre réservé. | `loans/validators.py::valider_qr` | Toute différence refuse l'emprunt ou le retour. |
| La création d'un emprunt diminue le stock. | `loans/services.py::creer_emprunt` | Le livre est verrouillé avec `select_for_update`. |
| Une réservation ne produit qu'un emprunt. | `Emprunt.reservation` | `OneToOneField` et statut `CONVERTED`. |
| Le retour normal restitue un exemplaire. | `enregistrer_retour` | Le stock ne dépasse jamais `stock_total`. |
| Un écart de poids impose une inspection. | `loans/validators.py::valider_poids`, `enregistrer_retour` | Le stock reste indisponible et une alerte est ouverte. |
| Le retard facturable exclut le délai de grâce. | `enregistrer_retour` | `max(0, jours_retard - delai_grace_jours)`. |
| Le tarif de retard est configurable. | `enregistrer_retour`, `ConfigurationBibliotheque.penalite_par_jour` | Montant = jours facturables × tarif journalier. |
| Un dommage ou une perte ouvre pénalité et rapport d'abus. | `enregistrer_retour` | Le livre passe en maintenance et le risque est recalculé. |
| Une pénalité met à jour le compteur et le risque. | `penalties/services.py::creer_penalite` | Notification et audit sont créés dans la même transaction. |
| Trois alertes ou un score de 75 bloquent le client. | `abuse/services.py::evaluer_niveau_risque` | `est_bloque=True` et `is_active=False`. |
| Toute opération sensible est auditée. | `audit/services.py::journaliser` | Acteur, cible, identifiant, détails et horodatage sont conservés. |
| Les pages sont séparées par rôle. | `accounts/permissions.py::roles_requis` | Un accès hors rôle retourne HTTP 403. |
| Le stock ne dépend pas uniquement de Python. | `loans/migrations/0003_mysql_stock_triggers.py`, `0004_mysql_loan_integrity.py` | MySQL décrémente à l'insertion et restitue au retour. |
| Une réservation active est unique par client et livre. | `Reservation.verrou_actif`, contrainte `reservation_active_unique` | Les statuts terminés utilisent `NULL`, autorisant l'historique tout en refusant deux lignes actives. |
| Une pénalité et son emprunt ont le même client. | `penalties/migrations/0003_mysql_penalty_integrity.py` | Un trigger rejette toute relation incohérente. |
| Une notification métier possède une preuve d'audit. | `Notification.journal_audit`, `notification_metier_auditee` | La FK est obligatoire pour tous les types non système. |
| Les statistiques ne sont jamais persistées ou codées en dur. | `stats/services.py` | Chaque affichage exécute des agrégations ORM sur les tables courantes. |
