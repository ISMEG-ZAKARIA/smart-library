from django.contrib.auth.models import UserManager


class RoleManager(UserManager):
    """Gestionnaire réutilisé par les profils proxy."""

    role = None

    def get_queryset(self):
        return super().get_queryset().filter(role=self.role)


class ClientManager(RoleManager):
    role = "CLIENT"


class BibliothecaireManager(RoleManager):
    role = "LIBRARIAN"


class AdministrateurManager(RoleManager):
    role = "ADMIN"

