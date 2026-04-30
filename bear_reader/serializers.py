from rest_framework import serializers

from .models import Note, NoteMatch


class NoteSerializer(serializers.Serializer):
    unique_id = serializers.CharField()
    title = serializers.CharField()
    body = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()
    archived = serializers.BooleanField()
    trashed = serializers.BooleanField()
    pinned = serializers.BooleanField()
    encrypted = serializers.BooleanField()

    def to_representation(self, instance: Note) -> dict:
        return {
            "unique_id": instance.unique_id,
            "title": instance.title,
            "body": instance.body,
            "tags": list(instance.tags),
            "created_at": instance.created_at.isoformat(),
            "modified_at": instance.modified_at.isoformat(),
            "archived": instance.archived,
            "trashed": instance.trashed,
            "pinned": instance.pinned,
            "encrypted": instance.encrypted,
        }


class NoteQuerySerializer(serializers.Serializer):
    tag = serializers.CharField(required=False, allow_blank=False)
    q = serializers.CharField(required=False, allow_blank=False)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=500)
    include_trashed = serializers.BooleanField(required=False, default=False)
    include_archived = serializers.BooleanField(required=False, default=True)


class NoteMatchSerializer(serializers.Serializer):
    note = NoteSerializer()
    score = serializers.FloatField()
    snippet = serializers.CharField()

    def to_representation(self, instance: NoteMatch) -> dict:
        return {
            "note": NoteSerializer(instance.note).data,
            "score": instance.score,
            "snippet": instance.snippet,
        }


class SearchQuerySerializer(serializers.Serializer):
    q = serializers.CharField(required=True, allow_blank=False)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=500)
    include_trashed = serializers.BooleanField(required=False, default=False)
    include_archived = serializers.BooleanField(required=False, default=True)
