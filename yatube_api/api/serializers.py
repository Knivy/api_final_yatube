"""Сериализаторы."""

from rest_framework import serializers  # type: ignore
from rest_framework.relations import SlugRelatedField  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from rest_framework.validators import UniqueTogetherValidator  # type: ignore

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


# Я перешла в 9 когорту и, возможно, поэтому
# Вам не видно обсуждений.
class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')
        # Нельзя дублировать подписки.
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            ),
        )

    def validate_following(self, following):
        """Проверка, на кого подписка."""
        if not hasattr(self, 'context'):
            raise serializers.ValidationError('Не передан контекст.')
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError('Не передан запрос.')
        if not hasattr(request, 'user'):
            raise serializers.ValidationError('Не передан пользователь.')
        if request.user == following:
            raise serializers.ValidationError('Нельзя подписаться на себя.')
        return following
