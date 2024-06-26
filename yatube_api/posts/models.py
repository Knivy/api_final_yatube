"""Модели."""

from django.contrib.auth import get_user_model  # type: ignore
from django.db import models  # type: ignore
from django.db.models import F, Q  # type: ignore

User = get_user_model()


class Group(models.Model):
    """Группы."""

    title = models.CharField(max_length=200,
                             verbose_name='Название')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг')
    description = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель поста."""

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True,
        verbose_name='Изображение')
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='group_posts',
        verbose_name='Группа', blank=True, null=True)

    class Meta:
        verbose_name = 'Посты'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Пост')
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарии'


class Follow(models.Model):
    """Подписки."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follows',
        verbose_name='Подписчик', editable=True,
        null=False, blank=False)
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers',
        verbose_name='На кого подписаны', editable=True,
        null=False, blank=False)

    class Meta:
        verbose_name = 'Подписки'
        # Может быть только одна связь между пользователями.
        unique_together = ('user', 'following')
        constraints = [
            # Нельзя подписаться на себя.
            models.CheckConstraint(
                check=~Q(user=F('following')),
                name='no_self_follow'
            ),
        ]
