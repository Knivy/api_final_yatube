"""Разрешения."""

from rest_framework.permissions import (  # type: ignore
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS, BasePermission)
from rest_framework.exceptions import MethodNotAllowed  # type: ignore


class IsAuthenticatedAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Безопасные методы для всех. Прочие - только авторство."""

    def has_object_permission(self, request, view, post_or_comment):
        """Проверка авторства."""
        return (post_or_comment.author == request.user
                if request.method not in SAFE_METHODS
                else True)


class ReadOnlyMethodsPermission(BasePermission):
    """Только чтение или ошибка 405 Метод не разрешён."""

    def has_permission(self, request, view):
        """Проверка метода."""
        if request.method not in SAFE_METHODS:
            raise MethodNotAllowed(request.method)
        return True
