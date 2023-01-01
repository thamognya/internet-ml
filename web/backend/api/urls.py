from typing import Any, List

from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns: list[Any] = [
    path("", views.APIView.as_view(), name="api"),
    path("nlp/", include("api.nlp.urls"), name="nlp api"),
]
