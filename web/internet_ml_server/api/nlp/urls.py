from typing import Any, List

from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns: list[Any] = [
    path("", views.NLPView.as_view(), name="nlp"),
    path("no-context/", include("api.nlp.nocontext.urls"), name="nlp no context api"),
]
