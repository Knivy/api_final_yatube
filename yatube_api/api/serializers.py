"""Сериализаторы."""

from rest_framework import serializers  # type: ignore
from rest_framework.relations import SlugRelatedField  # type: ignore
from rest_framework.fields import CurrentUserDefault  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore

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

    # def validate(self, data):
    #     user = serializers.CurrentUserDefault()
    #     print(data.keys())
    #     # request = self.context.get('request')
    #     # if not request:
    #     #     raise serializers.ValidationError(
    #     #           'Не получен запрос.')
    #     # data = request.POST.get('data')
    #     # print(data)
    #     # print(data.keys())
    #     following_name = (data.get('following') 
    #                       if data and isinstance(data, dict) else None)
    #     if not following_name:
    #         print('Не указано, на кого надо подписаться.')
    #         raise serializers.ValidationError(
    #               'Не указано, на кого надо подписаться.')
    #     if user.username == following_name:
    #         print('Нельзя подписаться на себя.')
    #         raise serializers.ValidationError(
    #               'Нельзя подписаться на себя.')
    #     following = get_object_or_404(
    #                 User, username=following_name)
    #     if user.follows.filter(following=following):
    #         print('Вы уже подписаны на этого пользователя.')
    #         raise serializers.ValidationError(
    #               'Вы уже подписаны на этого пользователя.')
    #     data['user'] = user
    #     data['following'] = following
    #     return data
    
    # def save(self, **kwargs):
    #     user = self.validated_data['user']
    #     following = self.validated_data['following']
    #     return super().save(user=user, following=following, **kwargs)
