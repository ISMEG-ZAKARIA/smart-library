"""Configuration du projet Smart Library."""

try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    # Django affichera une erreur explicite si les dépendances ne sont pas installées.
    pass

