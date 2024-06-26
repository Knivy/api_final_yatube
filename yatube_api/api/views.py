"""Контроллеры."""

from rest_framework import viewsets, generics, status, filters  # type: ignore
from rest_framework.pagination import LimitOffsetPagination  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.response import Response  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.http import JsonResponse, Http404  # type: ignore
from rest_framework.permissions import SAFE_METHODS  # type: ignore

from posts.models import Post, Group, Follow
from .serializers import (CommentSerializer, FollowSerializer,
                          PostSerializer, GroupSerializer)
from .permissions import IsAuthorOrReadOnly
from .exceptions import Error405

User = get_user_model()


class PermissionsMixin(viewsets.ModelViewSet):
    """Миксин разрешений."""

    permission_classes = (IsAuthorOrReadOnly,)


class PostViewSet(PermissionsMixin, viewsets.ModelViewSet):
    """Обработка постов."""

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создание поста."""
        serializer.save(author=self.request.user)


class CommentViewSet(PermissionsMixin, viewsets.ModelViewSet):
    """Обработка комментариев."""

    serializer_class = CommentSerializer

    def get_post(self):
        """Получение поста."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def perform_create(self, serializer):
        """Создание комментария."""
        serializer.save(author=self.request.user,
                        post=self.get_post())

    def get_queryset(self):
        """Выбор комментариев."""
        return self.get_post().comments.all()


class GroupViewSet(PermissionsMixin, viewsets.ReadOnlyModelViewSet):
    """Обработка групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED) 


class FollowView(generics.ListCreateAPIView):
    """Обработка подписок."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')

    def get_users(self):
        user = self.request.user
        username = user.username
        data = self.request.data
        if data and isinstance(data, dict):
            following_name = data.get('following')
            try:
                following = get_object_or_404(
                    User, username=following_name)
            except Exception:
                following = None
        else:
            following_name = None
            following = None
        return user, username, following, following_name

    def create(self, request, *args, **kwargs):
        user, username, following, following_name = self.get_users()
        if (not following or username == following_name
           or Follow.objects.filter(user=user, following=following)):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Создание подписки."""
        user, _, following, _ = self.get_users()
        serializer.save(user=user,
                        following=following)
        
    def get_queryset(self):
        """Список подписок пользователя."""
        return Follow.objects.filter(user=self.request.user)                 
    

def page_not_found(request, exception) -> JsonResponse:
    """Ошибка 404: Объект не найден."""
    return JsonResponse({"message": "Объект не найден."})
