from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def roles_requis(*roles):
    """Limite une vue aux rôles indiqués, avec support du superutilisateur."""
    def decorateur(vue):
        @login_required
        @wraps(vue)
        def enveloppe(request, *args, **kwargs):
            if not request.user.is_superuser and request.user.role not in roles:
                raise PermissionDenied("Votre rôle ne permet pas cette action.")
            return vue(request, *args, **kwargs)
        return enveloppe
    return decorateur

