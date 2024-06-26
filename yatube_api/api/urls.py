"""Адреса API."""

from django.urls import include, path  # type: ignore
from rest_framework import routers  # type: ignore
from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowView

app_name: str = 'api'

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')

v1_patterns: list[path] = [
    # path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('follow/', FollowView.as_view(), name='follows'),
    path('', include(router.urls)),
]

urlpatterns: list[path] = [
    path('v1/', include(v1_patterns)),
]
handler404 = 'api.views.page_not_found'
