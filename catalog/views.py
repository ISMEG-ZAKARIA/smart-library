from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Utilisateur
from accounts.permissions import roles_requis
from .forms import CommentaireForm, LivreForm
from .models import Livre
from .services import desactiver_livre, enregistrer_livre


@login_required
def catalogue(request):
    queryset = Livre.objects.filter(actif=True).select_related("categorie").prefetch_related("auteurs").annotate(
        popularite=Count("commentaires")
    )
    if request.user.est_client:
        queryset = queryset.filter(visible_client=True)
    q = request.GET.get("q", "").strip()
    categorie = request.GET.get("categorie", "")
    filtre = request.GET.get("filtre", "tous")
    if q:
        queryset = queryset.filter(Q(titre__icontains=q) | Q(isbn__icontains=q) | Q(auteurs__nom__icontains=q)).distinct()
    if categorie:
        queryset = queryset.filter(categorie_id=categorie)
    if request.user.est_client:
        if filtre == "disponibles":
            queryset = queryset.filter(stock_disponible__gt=0, statut=Livre.Statut.DISPONIBLE).order_by("titre")
        elif filtre == "populaires":
            queryset = queryset.order_by("-popularite", "titre")
        elif filtre == "nouveautes":
            queryset = queryset.order_by("-cree_le")
        else:
            queryset = queryset.order_by("titre")
    else:
        queryset = queryset.order_by("titre")
    return render(
        request,
        "catalog/catalogue.html",
        {"page_obj": Paginator(queryset, 12).get_page(request.GET.get("page")), "q": q, "filtre": filtre},
    )


@login_required
def detail(request, pk):
    queryset = Livre.objects.prefetch_related("auteurs", "commentaires__client")
    if request.user.est_client:
        queryset = queryset.filter(visible_client=True)
    livre = get_object_or_404(queryset, pk=pk)
    form = CommentaireForm(request.POST or None)
    if request.method == "POST" and request.user.est_client and form.is_valid():
        commentaire = form.save(commit=False)
        commentaire.client = request.user
        commentaire.livre = livre
        commentaire.save()
        messages.success(request, "Votre avis a été publié.")
        return redirect("catalog:detail", pk=pk)
    contexte = {"livre": livre, "form": form}
    if request.user.est_client:
        contexte.update(
            {
                "note_moyenne": livre.commentaires.aggregate(note=Avg("note"))["note"],
                "reservation_active": request.user.reservations.filter(livre=livre, statut="ACTIVE").exists(),
            }
        )
    return render(request, "catalog/detail.html", contexte)


@roles_requis(Utilisateur.Role.ADMIN, Utilisateur.Role.LIBRARIAN)
def livre_form(request, pk=None):
    livre = get_object_or_404(Livre, pk=pk) if pk else None
    form = LivreForm(request.POST or None, request.FILES or None, instance=livre)
    if request.method == "POST" and form.is_valid():
        livre = enregistrer_livre(form, request.user)
        messages.success(request, "Le catalogue a été mis à jour.")
        return redirect("catalog:detail", pk=livre.pk)
    return render(request, "base/formulaire.html", {"form": form, "titre": "Modifier le livre" if pk else "Ajouter un livre", "retour_url": "catalog:catalogue"})


@roles_requis(Utilisateur.Role.ADMIN, Utilisateur.Role.LIBRARIAN)
def desactiver(request, pk):
    if request.method == "POST":
        try:
            desactiver_livre(pk, request.user, request.POST.get("motif") or "Retrait du catalogue")
            messages.success(request, "Le livre a été retiré de tous les catalogues actifs.")
        except ValidationError as erreur:
            messages.error(request, " ".join(erreur.messages))
    return redirect("catalog:catalogue")
