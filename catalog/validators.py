import re
from django.core.exceptions import ValidationError


def valider_isbn(value):
    """Valide la longueur et la clé d'un ISBN-10 ou ISBN-13."""
    isbn = re.sub(r"[-\s]", "", value or "")
    if len(isbn) == 10:
        total = sum((10 - i) * (10 if c == "X" else int(c)) for i, c in enumerate(isbn) if c.isdigit() or c == "X")
        if len(isbn) != sum(c.isdigit() or c == "X" for c in isbn) or total % 11:
            raise ValidationError("ISBN-10 invalide.")
    elif len(isbn) == 13 and isbn.isdigit():
        total = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(isbn[:12]))
        if (10 - total % 10) % 10 != int(isbn[-1]):
            raise ValidationError("ISBN-13 invalide.")
    else:
        raise ValidationError("Saisissez un ISBN-10 ou ISBN-13 valide.")

