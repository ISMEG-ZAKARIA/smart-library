from .models import Notification


def notifications_non_lues(request):
    if request.user.is_authenticated:
        return {
            "nombre_notifications_non_lues": Notification.objects.filter(
                utilisateur=request.user,
                lue_le__isnull=True,
            ).count()
        }
    return {"nombre_notifications_non_lues": 0}
