from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from accounts.models import Utilisateur
from accounts.permissions import roles_requis
from .models import JournalAudit


@roles_requis(Utilisateur.Role.ADMIN)
def journal(request):
    queryset = JournalAudit.objects.select_related("acteur")
    q = request.GET.get("q", "").strip()
    if q:
        queryset = queryset.filter(Q(action__icontains=q) | Q(description_cible__icontains=q) | Q(acteur__email__icontains=q))
    return render(request, "audit/journal.html", {"page_obj": Paginator(queryset, 25).get_page(request.GET.get("page")), "q": q})

