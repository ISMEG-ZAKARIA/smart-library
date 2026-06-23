from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from accounts.models import Utilisateur
from accounts.permissions import roles_requis
from .forms import PenaliteForm
from .models import Penalite
from .services import annuler_penalite, creer_penalite, regler_penalite


@roles_requis(Utilisateur.Role.CLIENT, Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def liste(request):
    queryset = Penalite.objects.select_related("client", "emprunt__livre").order_by("-creee_le", "-id")
    if request.user.est_client:
        queryset = queryset.filter(client=request.user)
        contexte = {
            "penalites": queryset,
            "penalites_total": queryset.count(),
            "penalites_ouvertes": queryset.filter(statut=Penalite.Statut.OUVERTE).count(),
            "penalites_reglees": queryset.filter(statut=Penalite.Statut.REGLEE).count(),
            "montant_total": queryset.aggregate(total=Sum("montant"))["total"] or 0,
        }
        return render(request, "penalties/liste.html", contexte)
    return render(request, "penalties/liste.html", {"penalites": queryset})


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def creer(request):
    form = PenaliteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        donnees = form.cleaned_data
        try:
            penalite = creer_penalite(
                donnees["client"], donnees["emprunt"], donnees["type"], donnees["montant"], donnees["motif"], request.user
            )
        except ValidationError as erreur:
            form.add_error(None, erreur)
        else:
            messages.success(request, f"Pénalité #{penalite.pk} enregistrée et ajoutée à l’historique.")
            return redirect(f"{reverse('penalties:liste')}#historique-penalites")
    return render(request, "penalties/formulaire.html", {"form": form})


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def regler(request, pk):
    if request.method == "POST":
        penalite = get_object_or_404(Penalite, pk=pk)
        try:
            regler_penalite(penalite, request.user)
            messages.success(request, "La pénalité est marquée comme réglée.")
        except ValidationError as erreur:
            messages.error(request, " ".join(erreur.messages))
    return redirect("penalties:liste")


@roles_requis(Utilisateur.Role.LIBRARIAN, Utilisateur.Role.ADMIN)
def annuler(request, pk):
    if request.method == "POST":
        penalite = get_object_or_404(Penalite, pk=pk)
        try:
            annuler_penalite(penalite, request.user, request.POST.get("motif") or "Décision administrative")
            messages.success(request, "La pénalité a été annulée sans supprimer son historique.")
        except ValidationError as erreur:
            messages.error(request, " ".join(erreur.messages))
    return redirect("penalties:liste")
