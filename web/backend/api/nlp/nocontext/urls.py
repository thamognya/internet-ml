# type: ignore
from typing import Any, List

from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns: list[Any] = [
    path("question-answering/", views.QAView.as_view(), name="nlp"),
]
