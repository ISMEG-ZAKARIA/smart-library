from django.core.mail import send_mail
from django.utils import timezone
from .models import Notification


def notifier(utilisateur, titre, message, type_notification="SYSTEM", lien="", journal_audit=None):
    """Crée une notification interne et envoie un e-mail si le client l'autorise."""
    notification = Notification.objects.create(
        utilisateur=utilisateur,
        titre=titre,
        message=message,
        type=type_notification,
        lien=lien,
        journal_audit=journal_audit,
    )
    if utilisateur.notifications_email and utilisateur.email:
        send_mail(titre, message, None, [utilisateur.email], fail_silently=True)
    return notification


def marquer_comme_lue(notification, utilisateur):
    """Marque uniquement une notification appartenant à l'utilisateur connecté."""
    if notification.utilisateur_id != utilisateur.id:
        raise PermissionError("Cette notification ne vous appartient pas.")
    if not notification.lue_le:
        notification.lue_le = timezone.now()
        notification.save(update_fields=["lue_le"])
    return notification
