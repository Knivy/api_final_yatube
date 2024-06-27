"""Сериализаторы."""

from rest_framework import serializers  # type: ignore
from rest_framework.relations import SlugRelatedField  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from django.http import Http404  # type: ignore
from django.db.utils import IntegrityError  # type: ignore

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор групп."""

    class Meta:
        model = Group
        fields = '__all__'


class UserSerializerField(serializers.SlugRelatedField):
    def get_queryset(self):
        username = self.slug_field
        return User.objects.filter(username=username)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def get_request(self):
        request = None
        if self and hasattr(self, 'context'):
            request = self.context.get('request')
        if not request:
            raise serializers.ValidationError('Нет запроса.')
        return request
    
    def get_user(self):
        request = self.get_request()
        user = None
        if request and hasattr(request, 'user'):
            user = request.user
        return user

    def validate_user(self, value):
        user = self.get_user()
        if not user:
            raise serializers.ValidationError('Не указан подписчик.')
        return user
    
    def get_following(self):
        request = self.get_request()
        request_data = None
        if hasattr(request, 'data'):
            request_data = request.data
        following_name = None
        if request_data and isinstance(request_data, dict):
            following_name = request_data.get('following')
        if not following_name:
            raise serializers.ValidationError('Не указано, на кого подписка.')
        try:
            following = get_object_or_404(User, username=following_name)
        except Http404:
            raise serializers.ValidationError(
                'Нет пользователя, на кого подписка.')
        return following

    def validate(self, data_to_validate):
        """Валидация данных."""
        user = self.get_user()
        following = self.get_following()
        if user.username == following.username:
            raise serializers.ValidationError('Нельзя подписаться на себя.')
        if user.follows.filter(following=following):
            raise serializers.ValidationError('Подписка уже существует.')
        return data_to_validate

    def save(self, *args, **kwargs):
        """Сохранение подписки."""
        user = self.get_user()
        following = self.get_following()
        super().save(user=user,
                    following=following)
