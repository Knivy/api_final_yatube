"""Контроллеры."""

from rest_framework import viewsets, generics, status, filters  # type: ignore
from rest_framework.pagination import LimitOffsetPagination  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.response import Response  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.http import JsonResponse, Http404  # type: ignore
from rest_framework.exceptions import MethodNotAllowed  # type: ignore

from posts.models import Post, Group, Follow
from .serializers import (CommentSerializer, FollowSerializer,
                          PostSerializer, GroupSerializer)
from .permissions import IsAuthenticatedAuthorOrReadOnly

User = get_user_model()


class PermissionsMixin(viewsets.ModelViewSet):
    """Миксин разрешений."""

    permission_classes = (IsAuthenticatedAuthorOrReadOnly,)


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

    # Если убрать этот раздел, то падает 1 тест.
    # Тогда при попытке создать группу возвращается ошибка 400 вместо 405.
    def create(self, request):
        """Доступны только безопасные методы."""
        raise MethodNotAllowed('POST', 'Создание групп запрещено.')

    def update(self, request, pk=None):
        """Доступны только безопасные методы."""
        raise MethodNotAllowed('UPDATE', 'Замена групп запрещена.')

    def partial_update(self, request, pk=None):
        """Доступны только безопасные методы."""
        raise MethodNotAllowed('PUT', 'Редактирование групп запрещено.')

    def destroy(self, request, pk=None):
        """Доступны только безопасные методы."""
        raise MethodNotAllowed('DELETE', 'Удаление групп запрещено.')


class FollowView(generics.ListCreateAPIView):
    """Обработка подписок."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        """Список подписок пользователя."""
        return self.request.user.follows
    
    def perform_create(self, serializer):
        """Создание подписки."""
        user = self.request.user
        data = self.request.POST.get('data')
        following_name = data.get('following')
        following = get_object_or_404(User, username=following_name)
        serializer.save(user=user,
                        following=following)


def page_not_found(request, exception) -> JsonResponse:
    """Ошибка 404: Объект не найден."""
    return JsonResponse({"message": "Объект не найден."})
