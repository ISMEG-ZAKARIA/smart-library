from django.urls import path
from .views import centre

app_name = "abuse"
urlpatterns = [path("", centre, name="centre")]

