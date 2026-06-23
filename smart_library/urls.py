"""Routes principales de la plateforme."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("livres/", include("catalog.urls")),
    path("reservations/", include("reservations.urls")),
    path("emprunts/", include("loans.urls")),
    path("penalites/", include("penalties.urls")),
    path("notifications/", include("alerts.urls")),
    path("audit/", include("audit.urls")),
    path("abus/", include("abuse.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

