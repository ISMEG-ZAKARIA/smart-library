from .models import JournalAudit


def journaliser(acteur, action, cible, details=None, adresse_ip=None):
    """Écrit une trace uniforme pour toute opération métier sensible."""
    return JournalAudit.objects.create(
        acteur=acteur if getattr(acteur, "is_authenticated", False) else None,
        action=action,
        cible_type=cible._meta.label,
        cible_id=str(cible.pk),
        description_cible=str(cible)[:250],
        details=details or {},
        adresse_ip=adresse_ip,
    )

