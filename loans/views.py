from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Utilisateur
from accounts.permissions import roles_requis
from reservations.models import Reservation
from .forms import RetourForm, ValidationEmpruntForm
from .models import Emprunt
from .services import creer_emprunt, enregistrer_retour


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def validations(request):
    reservations = Reservation.objects.actives().select_related("client", "livre")
    return render(request, "loans/validations.html", {"reservations": reservations})


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def valider(request, reservation_id):
    reservation = get_object_or_404(Reservation.objects.select_related("livre"), pk=reservation_id)
    if request.method == "POST":
        try:
            creer_emprunt(reservation.id, request.POST.get("code_qr", ""), request.user)
            messages.success(request, "L'emprunt est validé et le stock a été mis à jour.")
        except ValidationError as erreur:
            messages.error(request, " ".join(erreur.messages))
    return redirect("loans:validations")


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def retours(request):
    emprunts = Emprunt.objects.actifs().select_related("client", "livre")
    return render(request, "loans/retours.html", {"emprunts": emprunts})


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def retour(request, pk):
    emprunt = get_object_or_404(Emprunt.objects.select_related("client", "livre"), pk=pk)
    form = RetourForm(request.POST or None, initial={"code_qr": emprunt.livre.code_qr})
    if request.method == "POST" and form.is_valid():
        try:
            resultat = enregistrer_retour(
                emprunt.id,
                form.cleaned_data["code_qr"],
                form.cleaned_data["poids_retour_grammes"],
                form.cleaned_data["etat_retour"],
                form.cleaned_data["commentaire_retour"],
                request.user,
            )
            if resultat.statut == Emprunt.Statut.INSPECTION:
                messages.warning(request, "Écart de poids détecté : le retour est placé en inspection.")
            else:
                messages.success(request, "Retour clôturé, stock et pénalités synchronisés.")
            return redirect("loans:retours")
        except ValidationError as erreur:
            messages.error(request, " ".join(erreur.messages))
    return render(request, "loans/retour_form.html", {"form": form, "emprunt": emprunt})


@roles_requis(Utilisateur.Role.CLIENT)
def historique(request):
    emprunts = request.user.emprunts.select_related("livre").prefetch_related("livre__auteurs").all()
    return render(
        request,
        "loans/historique.html",
        {
            "emprunts": emprunts,
            "total_emprunts": emprunts.count(),
            "emprunts_retournes": emprunts.filter(statut=Emprunt.Statut.RETOURNE).count(),
            "emprunts_actifs": emprunts.filter(statut=Emprunt.Statut.EN_COURS).count(),
            "emprunts_retard": emprunts.en_retard().count(),
        },
    )


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def suivi(request):
    """Affiche tous les emprunts persistés, actifs et terminés, au personnel."""
    emprunts = Emprunt.objects.select_related("client", "livre", "reservation", "valide_par").all()
    statut = request.GET.get("statut", "")
    if statut:
        emprunts = emprunts.filter(statut=statut)
    return render(request, "loans/suivi.html", {"emprunts": emprunts, "statuts": Emprunt.Statut.choices, "statut_actif": statut})
