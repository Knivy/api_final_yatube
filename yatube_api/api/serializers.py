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


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )
    following = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def save(self, *args, **kwargs):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if not user:
            raise serializers.ValidationError('Не указан подписчик.')
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
        try:
            super().save(user=user,
                        following=following)
        except IntegrityError:
            raise serializers.ValidationError('Нельзя сохранить подписку.')   
