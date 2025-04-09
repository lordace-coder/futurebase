from rest_framework.decorators import api_view
from core.models import Collection
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from client.serializers import CollectionSerializer
from collections_manager import manager
from bson import ObjectId  # Import ObjectId for handling MongoDB _id fields


class Credentials:
    user = None

    def __init__(self):
        self.user = None

    def validate(self, **kwargs):
        self.user = authenticate(
            self.request, username=kwargs.get("email"), password=kwargs.get("password")
        )
        return self.user is not None


class ListCollectionsApiView(ListAPIView, Credentials):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()

    def get(self, *args, **kwargs):
        if self.validate(**self.kwargs):
            print(self.user)
        else:
            return Response({"error": "invalid user"}, status=400)
        return super().get(*args, **kwargs)


class ListCollectionDataApiView(APIView, Credentials):
    def get(self, request, *args, **kwargs):
        self.validate(**kwargs)

        collection = Collection.objects.get(
            id=kwargs.get("id"), project__user=self.user
        )
        fields = collection.columns.all()
        collection_data = manager.fetchAllData(collection.dbName())

        # Convert ObjectId to string for JSON serialization
        collection_data = [
            {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in doc.items()}
            for doc in collection_data
        ]

        context = {
            "collection_data": collection_data,
            # "fields": fields,  # Get all columns/fields for this collection
        }
        return Response(context)
