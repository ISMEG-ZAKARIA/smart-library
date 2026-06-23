from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from reservations.models import Reservation
from .models import Notification
from .services import marquer_comme_lue


@login_required
def liste(request):
    notifications = Notification.objects.filter(utilisateur=request.user).select_related("journal_audit")
    contexte = {"notifications": notifications}
    if request.user.est_client:
        contexte.update(
            {
                "alertes_actives": notifications.filter(lue_le__isnull=True).count(),
                "reservations_expirees": request.user.reservations.filter(statut=Reservation.Statut.EXPIREE).count(),
            }
        )
    return render(request, "alerts/liste.html", contexte)


@login_required
def lire(request, pk):
    if request.method == "POST":
        notification = get_object_or_404(Notification, pk=pk, utilisateur=request.user)
        marquer_comme_lue(notification, request.user)
        if notification.lien and notification.lien.startswith("/"):
            return redirect(notification.lien)
    return redirect("alerts:liste")

