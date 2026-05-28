"""Locked-down mobile API surface for the cloud deployment.

Mounted only under ``gtd_site.urls_cloud`` (selected by ``GTD_ROOT_URLCONF`` on
Render). Exposes exactly four operations — list envs, read inbox, read next,
capture to inbox — and nothing else: every other route returns 404 because it
isn't wired up at all. These are dedicated views (not the permissive
``views.items``) so the surface can't be widened by query params.

A shared-secret passphrase (``settings.GTD_CLOUD_TOKEN``) guards every endpoint
except health, applied via the ``@cloud_token_required`` decorator so the gate
sits conspicuously above each view. When the token is empty the gate is
disabled (local default). When ``settings.GTD_CLOUD_SYNC`` is on, reads pull
from origin first and a successful capture commits + pushes back.
"""

import functools
import hmac
from collections.abc import Callable

from django.conf import settings
from django.utils.timezone import localdate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from gtd_core.cloud_sync import commit_and_push, pull_latest
from gtd_core.healthcheck import collect_health
from gtd_core.models import Bucket

from .serializers import CaptureSerializer, ItemSerializer
from .views import _require_env, _service  # canonical helpers — don't duplicate


def cloud_token_required(view: Callable[..., Response]) -> Callable[..., Response]:
    """Reject requests whose X-GTD-Token doesn't match the shared secret.

    No-op when GTD_CLOUD_TOKEN is empty so local dev needs no header. Uses a
    constant-time compare to avoid leaking the secret via timing. Returns 401
    (not DRF's default 403) so the mobile client knows to re-prompt for the
    passphrase.
    """

    @functools.wraps(view)
    def wrapper(request: Request, *args, **kwargs) -> Response:
        expected = settings.GTD_CLOUD_TOKEN
        if expected:
            provided = request.headers.get("X-GTD-Token", "")
            if not hmac.compare_digest(provided, expected):
                return Response({"error": "invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        return view(request, *args, **kwargs)

    return wrapper


@api_view(["GET"])
def mobile_health(request: Request) -> Response:
    info = collect_health()
    return Response({"ok": info.data_root.exists() and bool(info.envs)})


@api_view(["GET"])
@cloud_token_required
def mobile_list_envs(request: Request) -> Response:
    return Response([{"name": e} for e in _service().list_envs()])


@api_view(["GET"])
@cloud_token_required
def mobile_inbox(request: Request, env: str) -> Response:
    svc = _service()
    if missing := _require_env(svc, env):
        return missing
    if settings.GTD_CLOUD_SYNC:
        pull_latest(settings.BASE_DIR)
    items = svc.list_items(env, bucket=Bucket.INBOX)
    projects_by_id = {p.id: p for p in svc.list_projects(env, include_inactive=True)}
    return Response(
        ItemSerializer(
            items,
            many=True,
            context={"projects_by_id": projects_by_id, "today": localdate()},
        ).data
    )


@api_view(["GET"])
@cloud_token_required
def mobile_next(request: Request, env: str) -> Response:
    svc = _service()
    if missing := _require_env(svc, env):
        return missing
    if settings.GTD_CLOUD_SYNC:
        pull_latest(settings.BASE_DIR)
    items = svc.list_items(env, bucket=Bucket.NEXT, respect_next_cap=True)
    projects_by_id = {p.id: p for p in svc.list_projects(env, include_inactive=True)}
    return Response(
        ItemSerializer(
            items,
            many=True,
            context={"projects_by_id": projects_by_id, "today": localdate()},
        ).data
    )


@api_view(["POST"])
@cloud_token_required
def mobile_capture(request: Request, env: str) -> Response:
    svc = _service()
    if missing := _require_env(svc, env):
        return missing
    serializer = CaptureSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        item = svc.capture(env, **serializer.validated_data)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # On the ephemeral Render filesystem an un-pushed commit is lost on restart,
    # so report whether the capture actually reached GitHub rather than always
    # claiming success. `synced` is true when sync is off (nothing to push) or
    # the push succeeded; false means the item is local-only until a later sync.
    synced = True
    if settings.GTD_CLOUD_SYNC:
        result = commit_and_push(settings.BASE_DIR, message=f"mobile capture: {item.title}")
        synced = result.pushed

    payload = ItemSerializer(item).data
    payload["synced"] = synced
    return Response(payload, status=status.HTTP_201_CREATED)
