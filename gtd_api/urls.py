from django.urls import path

from . import views

urlpatterns = [
    path("envs/", views.list_envs),
    path("envs/<str:env>/config/", views.env_config),
    path("envs/<str:env>/items/", views.items),
    path("envs/<str:env>/items/<str:item_id>/", views.item_detail),
    path("envs/<str:env>/items/<str:item_id>/move/", views.item_move),
    path("envs/<str:env>/items/<str:item_id>/complete/", views.item_complete),
    path("envs/<str:env>/items/<str:item_id>/purge/", views.item_purge),
    path("envs/<str:env>/projects/", views.projects),
    path("envs/<str:env>/projects/<str:project_id>/", views.project_detail),
    path("snapshot/", views.snapshot_endpoint),
    path("snapshot/status/", views.snapshot_status_endpoint),
]
