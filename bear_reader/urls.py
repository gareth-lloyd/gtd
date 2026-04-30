from django.urls import path

from . import views

urlpatterns = [
    path("notes/", views.list_notes),
    path("notes/search/", views.search_notes),
    path("notes/<str:unique_id>/", views.get_note),
]
