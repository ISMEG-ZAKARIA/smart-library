"""Amorçage sûr de la base MySQL avant les commandes qui l'utilisent."""
import os


def ensure_mysql_database():
    """Crée PFA_3IIR si nécessaire, avec un encodage Unicode complet."""
    import pymysql

    connexion = pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "ImadZak2005@"),
        charset="utf8mb4",
        autocommit=True,
    )
    try:
        with connexion.cursor() as curseur:
            curseur.execute(
                "CREATE DATABASE IF NOT EXISTS `PFA_3IIR` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
    finally:
        connexion.close()

