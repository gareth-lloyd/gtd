from datetime import date

from django.conf import settings
from django.utils.timezone import localdate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from gtd_core.agent_launch import (
    AgentLaunchError,
    AgentLaunchNotConfiguredError,
)
from gtd_core.ai import (
    AiCaptureError,
    AiCaptureNoExtractionError,
    AiCaptureNotConfiguredError,
    AiCaptureUpstreamError,
)
from gtd_core.healthcheck import collect_health
from gtd_core.models import Bucket
from gtd_core.service import GtdService
from gtd_core.snapshot import snapshot, snapshot_status

from .serializers import (
    CaptureAiSerializer,
    CaptureSerializer,
    ItemPatchSerializer,
    ItemSerializer,
    MoveSerializer,
    ProjectCreateSerializer,
    ProjectPatchSerializer,
    ProjectReorderSerializer,
    ProjectSerializer,
    SnapshotRequestSerializer,
    TemplateSerializer,
)


def _service() -> GtdService:
    return GtdService(settings.GTD_DATA_ROOT, agent_cwd=settings.GTD_AGENT_CWD)


def _require_env(svc: GtdService, env: str) -> Response | None:
    if env not in svc.list_envs():
        return Response(status=status.HTTP_404_NOT_FOUND)
    return None


def _require_purge_confirmation(request: Request) -> Response | None:
    """Reject hard-deletes lacking the confirmation header — defends against scripted misclicks."""
    if request.headers.get("X-Confirm-Purge") != "true":
        return Response(
            {"error": "purge requires X-Confirm-Purge: true header"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None


@api_view(["GET"])
def health(request: Request) -> Response:
    info = collect_health()
    return Response(
        {
            "ok": info.data_root.exists() and bool(info.envs),
            "data_root": str(info.data_root),
            "envs": info.envs,
        }
    )


@api_view(["GET"])
def list_envs(request: Request) -> Response:
    return Response([{"name": e} for e in _service().list_envs()])


@api_view(["GET"])
def env_config(request: Request, env: str) -> Response:
    svc = _service()
    if missing := _require_env(svc, env):
        return missing
    cfg = svc.config(env)
    return Response(
        {
            "name": cfg.name,
            "contexts": cfg.contexts,
            "areas": cfg.areas,
            "default_energy": cfg.default_energy,
        }
    )


@api_view(["GET", "POST"])
def items(request: Request, env: str) -> Response:
    svc = _service()
    if missing := _require_env(svc, env):
        return missing
    if request.method == "GET":
        params = request.query_params
        bucket_name = params.get("status")
        try:
            bucket = Bucket(bucket_name) if bucket_name else None
        except ValueError:
            return Response(
                {"error": f"unknown bucket: {bucket_name!r}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Cap next-bucket lists by each project's `max_next_items`. Callers
        # can override with ?show_all=true to see every item (e.g. review).
        respect_next_cap = bucket is Bucket.NEXT and params.get("show_all") != "true"
        since_str = _qstr(params.get("since"))
        try:
            since = date.fromisoformat(since_str) if since_str else None
        except ValueError:
            return Response(
                {"error": f"invalid since: {since_str!r} (expected YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        filtered = svc.list_items(
            env,
            bucket=bucket,
            contexts=_parse_csv(params.get("contexts")),
            max_minutes=_parse_int(params.get("max_minutes")),
            min_minutes=_parse_int(params.get("min_minutes")),
            energy=_qstr(params.get("energy")),
            project=_qstr(params.get("project")),
            include_deferred=params.get("include_deferred") == "true",
            respect_next_cap=respect_next_cap,
            include_archive=params.get("include_archive") == "true",
            include_trash=params.get("include_trash") == "true",
            no_project=params.get("no_project") == "true",
            overdue=params.get("overdue") == "true",
            since=since,
        )
        projects_by_id = {p.id: p for p in svc.list_projects(env, include_inactive=True)}
        return Response(
            ItemSerializer(
                filtered,
                many=True,
                context={"projects_by_id": projects_by_id, "today": localdate()},
            ).data
        )

    serializer = CaptureSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        item = svc.capture(env, **serializer.validated_data)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def items_capture_ai(request: Request, env: str) -> Response:
    svc = _service()
    if missing := _require_env(svc, env):
        return missing
    serializer = CaptureAiSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        outcome = svc.capture_ai(
            env,
            serializer.validated_data["text"],
            model=getattr(settings, "ANTHROPIC_MODEL", ""),
        )
    except AiCaptureNotConfiguredError as e:
        return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except AiCaptureNoExtractionError as e:
        return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except AiCaptureUpstreamError as e:
        return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
    except AiCaptureError as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    projects_by_id = {p.id: p for p in svc.list_projects(env, include_inactive=True)}
    return Response(
        {
            "item": ItemSerializer(outcome.item, context={"projects_by_id": projects_by_id}).data,
            "summary": outcome.summary,
            "skipped_inbox": outcome.skipped_inbox,
            "project_title": outcome.project_title,
        },
        status=status.HTTP_201_CREATED,
    )


DONE_MAX_PAGE_SIZE = 200


@api_view(["GET"])
def items_done(request: Request, env: str) -> Response:
    svc = _service()
    if missing := _require_env(svc, env):
        return missing
    page = _parse_int(request.query_params.get("page"))
    page_size = _parse_int(request.query_params.get("page_size"))
    if page is None:
        page = 1
    if page_size is None:
        page_size = 50
    page_size = min(page_size, DONE_MAX_PAGE_SIZE)
    try:
        items, total = svc.list_done(env, page=page, page_size=page_size)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    projects_by_id = {p.id: p for p in svc.list_projects(env, include_inactive=True)}
    today = localdate()
    return Response(
        {
            "items": ItemSerializer(
                items,
                many=True,
                context={"projects_by_id": projects_by_id, "today": today},
            ).data,
            "page": page,
            "page_size": page_size,
            "total": total,
            "has_next": page * page_size < total,
        }
    )


@api_view(["GET", "PATCH", "DELETE"])
def item_detail(request: Request, env: str, item_id: str) -> Response:
    svc = _service()
    if request.method == "GET":
        item = svc.get_item(env, item_id)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ItemSerializer(item).data)

    if request.method == "PATCH":
        serializer = ItemPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            item = svc.update(env, item_id, serializer.validated_data)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ItemSerializer(item).data)

    try:
        item = svc.delete(env, item_id)
    except KeyError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ItemSerializer(item).data)


@api_view(["POST"])
def item_purge(request: Request, env: str, item_id: str) -> Response:
    if missing := _require_purge_confirmation(request):
        return missing
    try:
        _service().purge(env, item_id)
    except KeyError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def item_move(request: Request, env: str, item_id: str) -> Response:
    serializer = MoveSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        item = _service().move(env, item_id, Bucket(serializer.validated_data["to"]))
    except KeyError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ItemSerializer(item).data)


@api_view(["POST"])
def item_launch_agent(request: Request, env: str, item_id: str) -> Response:
    try:
        _service().launch_agent_session(env, item_id)
    except KeyError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except AgentLaunchNotConfiguredError as e:
        return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except AgentLaunchError as e:
        return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def item_complete(request: Request, env: str, item_id: str) -> Response:
    try:
        item = _service().complete(env, item_id)
    except KeyError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(ItemSerializer(item).data)


@api_view(["GET", "POST"])
def projects(request: Request, env: str) -> Response:
    svc = _service()
    if request.method == "GET":
        include_inactive = request.query_params.get("include_inactive") == "true"
        return Response(
            ProjectSerializer(
                svc.list_projects(env, include_inactive=include_inactive), many=True
            ).data
        )

    serializer = ProjectCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    project = svc.create_project(
        env,
        project_id=data["id"],
        title=data["title"],
        body=data.get("body", ""),
        outcome=data.get("outcome") or None,
        area=data.get("area") or None,
        tags=list(data.get("tags") or []),
        due=data.get("due") or None,
        priority=data.get("priority"),
        max_next_items=data.get("max_next_items"),
        working_dir=data.get("working_dir") or None,
    )
    return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def project_detail(request: Request, env: str, project_id: str) -> Response:
    svc = _service()
    if request.method == "GET":
        project = svc.get_project(env, project_id)
        if project is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        include_deferred = request.query_params.get("include_deferred") == "true"
        actions = svc.actions_for_project(env, project_id, include_deferred=include_deferred)
        return Response(
            {
                "project": ProjectSerializer(project).data,
                "actions": ItemSerializer(actions, many=True).data,
            }
        )

    if request.method == "PATCH":
        serializer = ProjectPatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            project = svc.update_project(env, project_id, serializer.validated_data)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProjectSerializer(project).data)

    if missing := _require_purge_confirmation(request):
        return missing
    try:
        svc.delete_project(env, project_id)
    except KeyError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def project_reorder(request: Request, env: str, project_id: str) -> Response:
    serializer = ProjectReorderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        items = _service().reorder_project_items(
            env, project_id, serializer.validated_data["item_ids"]
        )
    except KeyError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(ItemSerializer(items, many=True).data)


@api_view(["GET"])
def templates(request: Request, env: str) -> Response:
    svc = _service()
    if missing := _require_env(svc, env):
        return missing
    return Response(TemplateSerializer(svc.list_templates(env), many=True).data)


@api_view(["POST"])
def snapshot_endpoint(request: Request) -> Response:
    svc = _service()
    for env_name in svc.list_envs():
        svc.spawn_recurring(env_name)
        svc.clear_expired_defers(env_name)

    serializer = SnapshotRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    push = serializer.validated_data.get("push", False)
    result = snapshot(
        settings.BASE_DIR,
        message=serializer.validated_data.get("message") or None,
        push=push,
    )
    http_status = status.HTTP_502_BAD_GATEWAY if push and result.push_error else status.HTTP_200_OK
    return Response(
        {
            "committed": result.committed,
            "sha": result.sha,
            "files_changed": result.files_changed,
            "message": result.message,
            "pushed": result.pushed,
            "push_error": result.push_error,
        },
        status=http_status,
    )


@api_view(["GET"])
def snapshot_status_endpoint(request: Request) -> Response:
    result = snapshot_status(settings.BASE_DIR)
    return Response(
        {
            "dirty_count": result.dirty_count,
            "dirty_files": result.dirty_files,
            "unloadable_files": result.unloadable_files,
        }
    )


def _qstr(value: object) -> str | None:
    """Narrow a QueryDict.get() result to str | None.

    Django's QueryDict.get() returns Any (and DRF's QueryDict stub widens it
    further to `str | list | None`). Use this at the views layer when the
    value is single-valued and downstream code expects str | None.
    """
    return value if isinstance(value, str) else None


def _parse_csv(value: object) -> list[str] | None:
    s = _qstr(value)
    if not s:
        return None
    return [v.strip() for v in s.split(",") if v.strip()]


def _parse_int(value: object) -> int | None:
    s = _qstr(value)
    if not s:
        return None
    return int(s)
