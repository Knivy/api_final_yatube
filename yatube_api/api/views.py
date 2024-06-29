"""Контроллеры."""

from rest_framework import viewsets, generics, filters  # type: ignore
from rest_framework.pagination import LimitOffsetPagination  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.http import JsonResponse  # type: ignore

from posts.models import Post, Group
from .serializers import (CommentSerializer, FollowSerializer,
                          PostSerializer, GroupSerializer)
from .permissions import (IsAuthenticatedAuthorOrReadOnly,
                          ReadOnlyMethodsPermission)

User = get_user_model()


class PermissionsMixin(viewsets.ModelViewSet):
    """Миксин разрешений."""

    permission_classes = (IsAuthenticatedAuthorOrReadOnly,)


class PermissionsReadOnlyMixin(viewsets.ModelViewSet):
    """Миксин разрешений только на чтение."""

    permission_classes = (ReadOnlyMethodsPermission,)


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


class GroupViewSet(PermissionsReadOnlyMixin, viewsets.ReadOnlyModelViewSet):
    """Обработка групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowView(generics.ListCreateAPIView):
    """Обработка подписок."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Список подписок пользователя."""
        return self.request.user.follows.all()

    def perform_create(self, serializer):
        """Создание подписки."""
        user = self.request.user
        serializer.save(user=user)


def page_not_found(request, exception) -> JsonResponse:
    """Ошибка 404: Объект не найден."""
    return JsonResponse({"message": "Объект не найден."})
