from django.urls import path, re_path
from .views import proxy_view, clear_cache

urlpatterns = [
    path('clear_cache/', clear_cache),
    re_path(r'^(?P<path>.*)$', proxy_view),
]