# Cycle de vie de l'application

## Authentification

1. `accounts/views.py::inscription` valide `InscriptionForm` et crée un `Utilisateur` client.
2. Le signal `notifier_creation_compte` crée la notification de bienvenue.
3. `ConnexionView` délègue le contrôle du mot de passe à Django.
4. `accounts/views.py::accueil` sélectionne le tableau de bord selon le rôle.
5. `roles_requis` protège chaque action sensible.

## Réservation

1. Le client ouvre `books/detail.html` et poste vers `reservations:creer`.
2. `creer_reservation` vérifie rôle, compte, restriction, quota, doublon et stock.
3. `Livre` est verrouillé, la réservation est créée et la disponibilité recalculée.
4. Notification, audit, score de risque et signal sont synchronisés.
5. `expire_reservations` traite périodiquement les réservations non retirées.

## Emprunt

1. Le bibliothécaire consulte les réservations actives dans `loans/validations.html`.
2. Le QR scanné est comparé à `Livre.code_qr`.
3. `creer_emprunt` vérifie le quota, crée `Emprunt`, diminue le stock et convertit la réservation.
4. Le client reçoit l'échéance ; `JournalAudit` conserve l'opération.

## Retour

1. `loans/retour_form.html` présente QR, poids de référence, tolérance et échéance.
2. `enregistrer_retour` verrouille l'emprunt et le livre.
3. Un QR faux refuse le retour. Un poids non conforme passe l'emprunt en inspection et ouvre un rapport.
4. Un retour conforme ferme l'emprunt, restitue le stock et calcule le retard.
5. L'état endommagé/perdu place le livre en maintenance et ouvre les sanctions associées.

## Pénalité

1. Une pénalité naît automatiquement du retour ou manuellement via `PenaliteForm`.
2. `creer_penalite` enregistre montant et motif, met à jour le compteur et le risque, notifie et audite.
3. `regler_penalite` clôture une pénalité ouverte et recalcule le risque.

## Notification

`notifications/services.py::notifier` crée toujours une notification interne. Si la préférence du compte le permet, le même message part par e-mail. `marquer_comme_lue` vérifie la propriété avant modification.

## Détection d'abus

Les expirations, anomalies de poids, dommages et pertes créent un `RapportAbus`. `evaluer_niveau_risque` combine alertes, rapports graves et pénalités ouvertes. Trois alertes ou un score critique désactivent le compte. Une restriction administrative possède un type, un motif et une date de fin, puis est consultée dans les workflows futurs.

