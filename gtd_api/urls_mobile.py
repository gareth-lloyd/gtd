from django.urls import path

from . import mobile_views

urlpatterns = [
    path("health/", mobile_views.mobile_health),
    path("envs/", mobile_views.mobile_list_envs),
    path("envs/<str:env>/inbox/", mobile_views.mobile_inbox),
    path("envs/<str:env>/next/", mobile_views.mobile_next),
    path("envs/<str:env>/capture/", mobile_views.mobile_capture),
]
