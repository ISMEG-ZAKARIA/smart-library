from django.db import transaction
from .models import Utilisateur


@transaction.atomic
def basculer_blocage(utilisateur, acteur, motif):
    """Bloque ou débloque un compte et trace l'opération sensible."""
    from audit.services import journaliser
    from alerts.services import notifier

    utilisateur.est_bloque = not utilisateur.est_bloque
    utilisateur.is_active = not utilisateur.est_bloque
    utilisateur.save(update_fields=["est_bloque", "is_active"])
    etat = "bloqué" if utilisateur.est_bloque else "débloqué"
    audit = journaliser(acteur, f"COMPTE_{etat.upper()}", utilisateur, {"motif": motif})
    notifier(utilisateur, f"Compte {etat}", motif, "SECURITY", journal_audit=audit)
    return utilisateur


@transaction.atomic
def enregistrer_utilisateur(form, acteur):
    """Sauvegarde un compte et trace précisément les champs modifiés."""
    from audit.services import journaliser

    instance = form.instance
    creation = instance.pk is None
    avant = {}
    if not creation:
        courant = Utilisateur.objects.select_for_update().get(pk=instance.pk)
        avant = {champ: getattr(courant, champ) for champ in form.Meta.fields}
    utilisateur = form.save(commit=False)
    if creation:
        import uuid

        utilisateur.username = f"{utilisateur.email.split('@')[0]}-{uuid.uuid4().hex[:6]}"
    if form.cleaned_data.get("mot_de_passe"):
        utilisateur.set_password(form.cleaned_data["mot_de_passe"])
    utilisateur.save()
    apres = {champ: getattr(utilisateur, champ) for champ in form.Meta.fields}
    changements = {champ: {"avant": avant.get(champ), "apres": valeur} for champ, valeur in apres.items() if creation or avant.get(champ) != valeur}
    if creation:
        from audit.models import JournalAudit

        audit = JournalAudit.objects.filter(
            action="UTILISATEUR_CREE",
            cible_type=utilisateur._meta.label,
            cible_id=str(utilisateur.pk),
        ).order_by("-cree_le").first()
        if audit:
            audit.acteur = acteur
            audit.details = {"changements": changements, "origine": "interface_administration"}
            audit.save(update_fields=["acteur", "details"])
        else:
            journaliser(acteur, "UTILISATEUR_CREE", utilisateur, {"changements": changements})
    else:
        journaliser(acteur, "UTILISATEUR_MODIFIE", utilisateur, {"changements": changements})
    return utilisateur
