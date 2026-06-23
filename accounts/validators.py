import re
from django.core.exceptions import ValidationError


def valider_cin(value):
    """Accepte les CIN marocaines usuelles sans caractères dangereux."""
    if not re.fullmatch(r"[A-Za-z]{1,3}\d{4,10}", value or ""):
        raise ValidationError("Le CIN doit contenir 1 à 3 lettres suivies de 4 à 10 chiffres.")

