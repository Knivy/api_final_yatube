"""Адреса API."""

from django.urls import include, path  # type: ignore
from rest_framework import routers  # type: ignore
from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowView

app_name: str = 'api'

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowView, basename='follows')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')

v1_patterns: list[path] = [
    # По ТЗ не требуется добавление пользователей.
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]

urlpatterns: list[path] = [
    path('v1/', include(v1_patterns)),
]
