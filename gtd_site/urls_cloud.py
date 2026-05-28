"""Locked URL surface for the cloud (mobile) deployment.

Selected via GTD_ROOT_URLCONF=gtd_site.urls_cloud on Render. Mounts only the
slim mobile API plus the SPA fallback — the full gtd_api.urls, bear-api,
snapshot, projects and item mutations are deliberately absent, so they 404
rather than merely being denied.
"""

from django.urls import include, path, re_path

from .urls import spa_index

urlpatterns = [
    path("api/", include("gtd_api.urls_mobile")),
    # bear-api/ is excluded so it 404s instead of being swallowed by the SPA
    # fallback — keeps the "everything else closed off" guarantee crisp.
    re_path(r"^(?!api/|bear-api/|static/).*$", spa_index),
]
