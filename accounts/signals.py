from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Utilisateur


@receiver(post_save, sender=Utilisateur)
def notifier_creation_compte(sender, instance, created, **kwargs):
    """Souhaite la bienvenue au nouveau compte sans dupliquer les notifications."""
    if created:
        from audit.services import journaliser
        from alerts.services import notifier

        audit = journaliser(None, "UTILISATEUR_CREE", instance, {"origine": "signal_post_save"})
        notifier(
            instance,
            "Bienvenue sur Smart Library",
            "Votre compte est prêt. Vous pouvez consulter le catalogue.",
            "SYSTEM",
            journal_audit=audit,
        )
