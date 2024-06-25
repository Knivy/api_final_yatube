"""Разрешения."""

from rest_framework.permissions import (BasePermission,  # type: ignore
                                        SAFE_METHODS)


class IsAuthorOrReadOnly(BasePermission):
    """Безопасные методы для всех. Прочие - только авторство."""

    def has_object_permission(self, request, view, post_or_comment):
        return (post_or_comment.author == request.user
                if request.method not in SAFE_METHODS
                else True)

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated
