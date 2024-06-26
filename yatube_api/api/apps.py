"""Настройки приложения API."""

from django.apps import AppConfig  # type: ignore


class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = 'API'
