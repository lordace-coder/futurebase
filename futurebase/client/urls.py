from django.urls import path
from . import views


urlpatterns = [
    path(
        "collections/<str:email>/<str:password>/<int:project_id>",
        views.ListCollectionsApiView.as_view(),
    ),
    path(
        "collection-data/<str:email>/<str:password>/<int:id>",
        views.ListCollectionDataApiView.as_view(),
    ),
    path(
        "collections/",
        views.ListCollectionsApiView.as_view(),
    ),
    path("collection-actions/<str:email>/<str:password>/<int:id>",
        views.CollectionsActionsApiView.as_view(),
    ),
]
