from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from audit.models import JournalAudit
from loans.models import Emprunt
from penalties.models import Penalite
from .forms import ClientParametresForm, ConfigurationForm, ConnexionForm, InscriptionForm, ProfilForm, UtilisateurForm
from .models import ConfigurationBibliotheque, Utilisateur
from .permissions import roles_requis
from .services import basculer_blocage, enregistrer_utilisateur
from dashboard.services import (
    repartition_emprunts,
    repartition_penalites,
    repartition_reservations,
    statistiques_admin,
    statistiques_bibliothecaire,
    statistiques_client,
    statistiques_par_livre,
    tendances_emprunts,
)


class ConnexionView(LoginView):
    template_name = "accounts/connexion.html"
    authentication_form = ConnexionForm
    redirect_authenticated_user = True


class DeconnexionView(LogoutView):
    pass


def inscription(request):
    if request.user.is_authenticated:
        return redirect("accounts:accueil")
    form = InscriptionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        utilisateur = form.save(commit=False)
        utilisateur.role = Utilisateur.Role.CLIENT
        utilisateur.save()
        login(request, utilisateur)
        messages.success(request, "Votre compte Smart Library a été créé.")
        return redirect("accounts:accueil")
    return render(request, "accounts/inscription.html", {"form": form})


@login_required
def accueil(request):
    if request.user.est_administrateur:
        contexte = statistiques_admin()
        contexte.update({
            "audits": contexte["activites_recentes"][:6],
            "risques": Utilisateur.objects.filter(role=Utilisateur.Role.CLIENT).annotate(
                total_penalites=Count("penalites", filter=~Q(penalites__statut=Penalite.Statut.ANNULEE))
            ).order_by("-score_risque")[:5],
        })
        return render(request, "admin_interface/dashboard.html", contexte)
    if request.user.est_bibliothecaire:
        contexte = statistiques_bibliothecaire()
        contexte["emprunts_recents"] = Emprunt.objects.select_related("client", "livre")[:6]
        return render(request, "librarian_interface/dashboard.html", contexte)
    contexte = statistiques_client(request.user)
    contexte["emprunts_recents"] = request.user.emprunts.select_related("livre")[:5]
    return render(request, "client_interface/dashboard.html", contexte)


@login_required
def profil(request):
    if request.user.est_client:
        if request.method == "POST":
            return redirect("accounts:client_parametres")
        contexte = statistiques_client(request.user)
        contexte.update(
            {
                "reservations_total": request.user.reservations.count(),
                "emprunts_total": request.user.emprunts.count(),
                "commentaires_total": request.user.commentaires.count(),
                "activites_recentes": JournalAudit.objects.filter(acteur=request.user)[:6],
            }
        )
        return render(request, "accounts/client_profil.html", contexte)

    form = ProfilForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        avant = {champ: getattr(request.user, champ) for champ in form.Meta.fields}
        utilisateur = form.save()
        changements = {
            champ: {"avant": avant[champ], "apres": getattr(utilisateur, champ)}
            for champ in form.Meta.fields
            if avant[champ] != getattr(utilisateur, champ)
        }
        if changements:
            from audit.services import journaliser

            journaliser(request.user, "PROFIL_MODIFIE", utilisateur, {"changements": changements})
        messages.success(request, "Votre profil a été mis à jour.")
        return redirect("accounts:profil")
    return render(request, "accounts/profil.html", {"form": form})


@roles_requis(Utilisateur.Role.CLIENT)
def client_parametres(request):
    form = ClientParametresForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        avant = {champ: getattr(request.user, champ) for champ in form.Meta.fields}
        utilisateur = form.save()
        changements = {
            champ: {"avant": avant[champ], "apres": getattr(utilisateur, champ)}
            for champ in form.Meta.fields
            if avant[champ] != getattr(utilisateur, champ)
        }
        if changements:
            from audit.services import journaliser

            journaliser(request.user, "PROFIL_MODIFIE", utilisateur, {"changements": changements})
        messages.success(request, "Vos paramètres ont été enregistrés.")
        return redirect("accounts:client_parametres")
    return render(request, "accounts/client_parametres.html", {"form": form})


@roles_requis(Utilisateur.Role.ADMIN)
def utilisateurs(request):
    queryset = Utilisateur.objects.annotate(
        total_penalites=Count("penalites", filter=~Q(penalites__statut=Penalite.Statut.ANNULEE))
    )
    recherche = request.GET.get("q", "").strip()
    role = request.GET.get("role", "")
    statut = request.GET.get("statut", "")
    if recherche:
        queryset = queryset.filter(Q(first_name__icontains=recherche) | Q(last_name__icontains=recherche) | Q(email__icontains=recherche) | Q(cin__icontains=recherche))
    if role:
        queryset = queryset.filter(role=role)
    if statut == "actif":
        queryset = queryset.filter(is_active=True, est_bloque=False)
    elif statut == "bloque":
        queryset = queryset.filter(est_bloque=True)
    page = Paginator(queryset.order_by("last_name", "first_name", "id"), 15).get_page(request.GET.get("page"))
    return render(request, "admin_interface/utilisateurs.html", {"page_obj": page, "roles": Utilisateur.Role.choices, "recherche": recherche, "role_actif": role, "statut_actif": statut})


@roles_requis(Utilisateur.Role.ADMIN)
def utilisateur_form(request, pk=None):
    utilisateur = get_object_or_404(Utilisateur, pk=pk) if pk else None
    form = UtilisateurForm(request.POST or None, instance=utilisateur)
    if request.method == "POST" and form.is_valid():
        enregistrer_utilisateur(form, request.user)
        messages.success(request, "Utilisateur enregistré.")
        return redirect("accounts:utilisateurs")
    return render(request, "base/formulaire.html", {"form": form, "titre": "Modifier l'utilisateur" if pk else "Nouvel utilisateur", "retour_url": "accounts:utilisateurs"})


@roles_requis(Utilisateur.Role.ADMIN)
def bloquer_utilisateur(request, pk):
    if request.method == "POST":
        utilisateur = get_object_or_404(Utilisateur, pk=pk)
        motif = request.POST.get("motif", "Décision administrative")
        basculer_blocage(utilisateur, request.user, motif)
        messages.success(request, "Le statut du compte a été mis à jour.")
    return redirect("accounts:utilisateurs")


@roles_requis(Utilisateur.Role.ADMIN)
def parametres(request):
    configuration = ConfigurationBibliotheque.charger()
    form = ConfigurationForm(request.POST or None, instance=configuration)
    if request.method == "POST" and form.is_valid():
        form.save()
        from audit.services import journaliser
        journaliser(request.user, "CONFIGURATION_MODIFIEE", configuration)
        messages.success(request, "Les règles de la bibliothèque ont été enregistrées.")
        return redirect("accounts:parametres")
    return render(request, "admin_interface/parametres.html", {"form": form, "configuration": configuration})


@roles_requis(Utilisateur.Role.ADMIN)
def statistiques(request):
    contexte = statistiques_admin()
    contexte.update({
        "tendances": tendances_emprunts(),
        "statistiques_livres": statistiques_par_livre()[:10],
        "repartition_penalites": repartition_penalites(),
        "repartition_emprunts": repartition_emprunts(),
        "repartition_reservations": repartition_reservations(),
    })
    return render(request, "admin_interface/statistiques.html", contexte)
