from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound
from django.urls import include, path, re_path


def spa_index(request):
    index = settings.FRONTEND_DIR / "index.html"
    if not index.exists():
        return HttpResponseNotFound(
            "Frontend not built. Run `cd frontend && npm run build`."
        )
    return FileResponse(index.open("rb"), content_type="text/html")


urlpatterns = [
    path("api/", include("gtd_api.urls")),
    re_path(r"^(?!api/|static/).*$", spa_index),
]
