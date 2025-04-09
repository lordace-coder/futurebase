from rest_framework import serializers
from core.models import Project, Collection, Column


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ["id", "name", "field"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "user", "title", "description", "created_at"]


class CollectionSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True)

    class Meta:
        model = Collection
        fields = ["id", "project", "name", "columns"]
