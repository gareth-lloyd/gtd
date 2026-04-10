from django.urls import include, path

urlpatterns = [
    path("api/", include("gtd_api.urls")),
]
