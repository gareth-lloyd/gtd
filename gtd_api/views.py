from datetime import datetime

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from gtd_core.models import Bucket, Project
from gtd_core.service import GtdService
from gtd_core.snapshot import snapshot, snapshot_status

from .serializers import (
    CaptureSerializer,
    ItemSerializer,
    MoveSerializer,
    ProjectCreateSerializer,
    ProjectSerializer,
    SnapshotRequestSerializer,
)


def _service() -> GtdService:
    return GtdService(settings.GTD_DATA_ROOT)


@api_view(["GET"])
def list_envs(request: Request) -> Response:
    return Response([{"name": e} for e in _service().list_envs()])


@api_view(["GET"])
def env_config(request: Request, env: str) -> Response:
    svc = _service()
    if env not in svc.list_envs():
        return Response(status=status.HTTP_404_NOT_FOUND)
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
    if request.method == "GET":
        params = request.query_params
        bucket_name = params.get("status")
        bucket = Bucket(bucket_name) if bucket_name else None
        item_list = svc.repo(env).list_items(bucket=bucket)
        filtered = svc.filter_items(
            item_list,
            contexts=_parse_csv(params.get("contexts")),
            max_minutes=_parse_int(params.get("max_minutes")),
            energy=params.get("energy"),
            project=params.get("project"),
            include_deferred=params.get("include_deferred") == "true",
        )
        return Response(ItemSerializer(filtered, many=True).data)

    serializer = CaptureSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    item = svc.capture(env, **serializer.validated_data)
    return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def item_detail(request: Request, env: str, item_id: str) -> Response:
    svc = _service()
    if request.method == "GET":
        item = svc.repo(env).get(item_id)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ItemSerializer(item).data)

    if request.method == "PATCH":
        try:
            item = svc.update(env, item_id, request.data)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ItemSerializer(item).data)

    try:
        svc.delete(env, item_id)
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
        return Response(ProjectSerializer(svc.list_projects(env), many=True).data)

    serializer = ProjectCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    now = datetime.now()
    data = serializer.validated_data
    project = Project(
        id=data["id"],
        title=data["title"],
        body=data.get("body", ""),
        created=now,
        updated=now,
        outcome=data.get("outcome") or None,
        area=data.get("area") or None,
        tags=list(data.get("tags") or []),
    )
    svc.save_project(env, project)
    return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def project_detail(request: Request, env: str, project_id: str) -> Response:
    svc = _service()
    project = svc.get_project(env, project_id)
    if project is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    actions = svc.actions_for_project(env, project_id)
    return Response(
        {
            "project": ProjectSerializer(project).data,
            "actions": ItemSerializer(actions, many=True).data,
        }
    )


@api_view(["POST"])
def snapshot_endpoint(request: Request) -> Response:
    serializer = SnapshotRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = snapshot(
        settings.BASE_DIR,
        message=serializer.validated_data.get("message") or None,
        push=serializer.validated_data.get("push", False),
    )
    return Response(
        {
            "committed": result.committed,
            "sha": result.sha,
            "files_changed": result.files_changed,
            "message": result.message,
            "pushed": result.pushed,
        }
    )


@api_view(["GET"])
def snapshot_status_endpoint(request: Request) -> Response:
    result = snapshot_status(settings.BASE_DIR)
    return Response(
        {
            "dirty_count": result.dirty_count,
            "dirty_files": result.dirty_files,
        }
    )


def _parse_csv(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [v.strip() for v in value.split(",") if v.strip()]


def _parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(value)
