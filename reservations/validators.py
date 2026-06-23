from django.core.exceptions import ValidationError


def valider_client_reservable(client):
    from django.utils import timezone
    from abuse.models import Restriction

    if not client.est_client:
        raise ValidationError("Seul un client peut réserver un ouvrage.")
    if client.est_bloque or not client.is_active:
        raise ValidationError("Ce compte est bloqué et ne peut pas réserver.")
    if client.restrictions.filter(
        active=True,
        type__in=[Restriction.Type.EMPRUNTS, Restriction.Type.COMPTE],
        fin__gt=timezone.now(),
    ).exists():
        raise ValidationError("Une restriction active interdit actuellement les réservations et emprunts.")
