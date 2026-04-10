from rest_framework import serializers


class ItemSerializer(serializers.Serializer):
    """Read-only representation of a gtd_core.models.Item."""

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "body": instance.body,
            "created": instance.created.isoformat() if instance.created else None,
            "updated": instance.updated.isoformat() if instance.updated else None,
            "status": instance.status.value,
            "contexts": list(instance.contexts),
            "energy": instance.energy,
            "time_minutes": instance.time_minutes,
            "project": instance.project,
            "area": instance.area,
            "tags": list(instance.tags),
            "due": instance.due.isoformat() if instance.due else None,
            "defer_until": instance.defer_until.isoformat() if instance.defer_until else None,
            "waiting_on": instance.waiting_on,
            "waiting_since": instance.waiting_since.isoformat() if instance.waiting_since else None,
        }


class ProjectSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "body": instance.body,
            "created": instance.created.isoformat(),
            "updated": instance.updated.isoformat(),
            "status": instance.status,
            "outcome": instance.outcome,
            "area": instance.area,
            "tags": list(instance.tags),
        }


class CaptureSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField(allow_blank=True, default="")


class MoveSerializer(serializers.Serializer):
    to = serializers.ChoiceField(
        choices=["inbox", "next", "waiting", "someday", "reference", "archive"]
    )


class ProjectCreateSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    body = serializers.CharField(allow_blank=True, default="")
    outcome = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    area = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list)


class SnapshotRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    push = serializers.BooleanField(default=False)
