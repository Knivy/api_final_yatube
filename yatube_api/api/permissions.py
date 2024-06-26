"""Разрешения."""

from rest_framework.permissions import (  # type: ignore
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS)


class IsAuthenticatedAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """Безопасные методы для всех. Прочие - только авторство."""

    def has_object_permission(self, request, view, post_or_comment):
        return (post_or_comment.author == request.user
                if request.method not in SAFE_METHODS
                else True)
