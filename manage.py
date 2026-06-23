#!/usr/bin/env python
"""Point d'entrée des commandes d'administration Smart Library."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_library.settings")

    commande = sys.argv[1] if len(sys.argv) > 1 else ""
    commandes_avec_base = {"migrate", "runserver", "createsuperuser", "loaddata", "seed_demo"}
    if commande in commandes_avec_base and os.getenv("USE_SQLITE_FOR_TESTS") != "1":
        from smart_library.database import ensure_mysql_database

        ensure_mysql_database()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

