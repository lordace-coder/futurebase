from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('create-project/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/create-collection/', views.create_collection, name='create_collection'),
    path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:project_id>/collection/<int:collection_id>/edit/', views.edit_collection, name='edit_collection'),
    path('collection/<int:collection_id>',views.collection_detail_view,name='collection-detail'),
    path('collection/<int:collection_id>/add-data/', views.collection_detail_view, name='add_collection_data'),
    path('edit-collection-item/<str:collection_id>/<str:item_id>',views.edit_collection_item,name = 'edit-collection-item'),
    path('delete-collection-item/<str:collection_id>/<str:item_id>',views.delete_collection_item,name = 'delete-collection-item')
] 