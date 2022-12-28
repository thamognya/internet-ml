from typing import Any, List

from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns: list[Any] = [
    path("", views.ApiView.as_view()),
    path("question-answer/", include("api.question_answer.urls")),
]
