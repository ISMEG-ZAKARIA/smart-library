from django.urls import path
from .views import journal

app_name = "audit"
urlpatterns = [path("", journal, name="journal")]

