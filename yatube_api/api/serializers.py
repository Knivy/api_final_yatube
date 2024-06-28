"""Сериализаторы."""

from rest_framework import serializers  # type: ignore
from rest_framework.relations import SlugRelatedField  # type: ignore
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


class UserSerializerField(serializers.SlugRelatedField):
    def get_queryset(self):
        username = self.slug_field
        return User.objects.filter(username=username)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    # Эти поля только для чтения, потому что
    # SlugRelatedField проблематично реализовать иначе.
    # Если бы и удалось, в данных методов валидации сериализатора
    # не было бы данных о user и нужно было бы доставать из request.
    # Поэтому валидация в модели, а не сериализаторе.
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'following')
