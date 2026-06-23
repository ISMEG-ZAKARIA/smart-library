from django.core.exceptions import ValidationError


def valider_qr(livre, code_qr):
    """Refuse un scan qui ne correspond pas exactement à l'ouvrage attendu."""
    if str(livre.code_qr) != str(code_qr).strip():
        raise ValidationError("Le QR code ne correspond pas au livre réservé.")


def valider_poids(livre, poids_mesure):
    """Retourne vrai si l'écart de poids reste dans la tolérance configurée."""
    return abs(livre.poids_reference_grammes - poids_mesure) <= livre.tolerance_poids_grammes

