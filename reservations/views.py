from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Utilisateur
from accounts.permissions import roles_requis
from .models import Reservation
from .services import annuler_reservation, creer_reservation, refuser_reservation


@roles_requis(Utilisateur.Role.CLIENT)
def liste(request):
    reservations = request.user.reservations.select_related("livre", "livre__categorie").prefetch_related("livre__auteurs").all()
    return render(
        request,
        "reservations/liste.html",
        {
            "reservations": reservations,
            "reservations_actives": reservations.filter(statut=Reservation.Statut.ACTIVE).count(),
            "reservations_expirees": reservations.filter(statut=Reservation.Statut.EXPIREE).count(),
        },
    )


@roles_requis(Utilisateur.Role.CLIENT)
def creer(request, livre_id):
    if request.method == "POST":
        try:
            creer_reservation(request.user, livre_id)
            messages.success(request, "Votre réservation est confirmée.")
        except ValidationError as erreur:
            messages.error(request, " ".join(erreur.messages))
    return redirect("catalog:detail", pk=livre_id)


@roles_requis(Utilisateur.Role.CLIENT)
def annuler(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, client=request.user)
    if request.method == "POST":
        try:
            annuler_reservation(reservation, request.user, request.POST.get("motif") or "Annulation demandée par le client")
            messages.success(request, "La réservation a été annulée.")
        except ValidationError as erreur:
            messages.error(request, " ".join(erreur.messages))
    return redirect("reservations:liste")


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def suivi(request):
    """Expose la table unique des réservations au personnel autorisé."""
    reservations = Reservation.objects.select_related("client", "livre", "traitee_par").all()
    statut = request.GET.get("statut", "")
    if statut:
        reservations = reservations.filter(statut=statut)
    return render(request, "reservations/suivi.html", {"reservations": reservations, "statuts": Reservation.Statut.choices, "statut_actif": statut})


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def refuser(request, pk):
    if request.method == "POST":
        reservation = get_object_or_404(Reservation, pk=pk)
        try:
            refuser_reservation(reservation, request.user, request.POST.get("motif") or "Demande non conforme aux règles de prêt")
            messages.success(request, "La réservation a été refusée et le client notifié.")
        except ValidationError as erreur:
            messages.error(request, " ".join(erreur.messages))
    return redirect("reservations:suivi")
