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
            "order": instance.order,
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
            "due": instance.due.isoformat() if instance.due else None,
            "priority": instance.priority,
            "sequential": instance.sequential,
        }


class CaptureSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField(allow_blank=True, default="")
    energy = serializers.ChoiceField(
        choices=["low", "medium", "high"], required=False, allow_null=True
    )
    time_minutes = serializers.IntegerField(required=False, allow_null=True)
    contexts = serializers.ListField(
        child=serializers.CharField(), required=False
    )


class MoveSerializer(serializers.Serializer):
    to = serializers.ChoiceField(
        choices=["inbox", "next", "waiting", "someday", "reference", "archive", "trash"]
    )


class ProjectCreateSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    body = serializers.CharField(allow_blank=True, default="")
    outcome = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    area = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    due = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    priority = serializers.IntegerField(required=False, allow_null=True, min_value=1, max_value=5)
    sequential = serializers.BooleanField(required=False)


class ItemPatchSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    body = serializers.CharField(required=False, allow_blank=True)
    contexts = serializers.ListField(child=serializers.CharField(), required=False)
    energy = serializers.ChoiceField(
        choices=["low", "medium", "high"], required=False, allow_null=True
    )
    time_minutes = serializers.IntegerField(required=False, allow_null=True)
    area = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    project = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    due = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    defer_until = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    waiting_on = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    order = serializers.IntegerField(required=False, allow_null=True)


class ProjectPatchSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    body = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(
        choices=["active", "on_hold", "complete", "dropped"], required=False
    )
    outcome = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    area = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    due = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    priority = serializers.IntegerField(required=False, allow_null=True, min_value=1, max_value=5)
    sequential = serializers.BooleanField(required=False)


class ProjectReorderSerializer(serializers.Serializer):
    item_ids = serializers.ListField(child=serializers.CharField(), allow_empty=False)


class SnapshotRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    push = serializers.BooleanField(default=False)
