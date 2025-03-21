from . import views
from django.urls import path

urlpatterns = [
    path('login/',views.index,name='home'),
    path('signup/',views.register,name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path('',views.dashboard,name='dashboard'),
    path('create-project/',views.create_project,name='create_project'),
]