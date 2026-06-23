from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from accounts.models import Utilisateur
from accounts.permissions import roles_requis
from penalties.models import Penalite
from .forms import RestrictionForm
from .models import RapportAbus, Restriction
from .services import appliquer_restriction
from dashboard.services import statistiques_admin


@roles_requis(Utilisateur.Role.ADMIN)
def centre(request):
    form = RestrictionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        appliquer_restriction(
            form.cleaned_data["utilisateur"], form.cleaned_data["type"], form.cleaned_data["motif"], form.cleaned_data["duree_jours"], request.user
        )
        messages.success(request, "La restriction a été appliquée, notifiée et journalisée.")
        return redirect("abuse:centre")
    globales = statistiques_admin()
    contexte = {
        "form": form,
        "utilisateurs_risque": Utilisateur.objects.filter(role=Utilisateur.Role.CLIENT, score_risque__gte=40).annotate(
            total_penalites=Count("penalites", filter=~Q(penalites__statut=Penalite.Statut.ANNULEE))
        ).order_by("-score_risque")[:4],
        "alertes": RapportAbus.objects.filter(statut=RapportAbus.Statut.OUVERT).select_related("client")[:8],
        "total_alertes": globales["rapports_abus_ouverts"],
        "restrictions_attente": globales["restrictions_actives"],
        "penalites": Penalite.objects.select_related("client").order_by("-creee_le", "-id")[:8],
        "total_ouvert": globales["montant_penalites_ouvertes"],
    }
    return render(request, "admin_interface/abus.html", contexte)
