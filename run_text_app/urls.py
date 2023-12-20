from django.urls import path

from .views import run_text, home

urlpatterns = [
    path("runtext/", run_text, name="run_text"),
    path("", home, name="home")
]
