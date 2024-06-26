"""Приложение постов."""

from django.apps import AppConfig  # type: ignore


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = 'Посты'
