from django.urls import path

from .views import run_text

urlpatterns = [
    path("runtext/", run_text, name="run_text"),
]
