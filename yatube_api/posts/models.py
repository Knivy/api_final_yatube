"""Модели."""

from django.contrib.auth import get_user_model  # type: ignore
from django.db import models  # type: ignore

User = get_user_model()


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

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Посты'


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


class Group(models.Model):
    """Группы."""

    title = models.CharField(max_length=200,
                             verbose_name='Название')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг')
    description = models.TextField(
        verbose_name='Описание',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группы'


class Follow(models.Model):
    """Подписки."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follows',
        verbose_name='Подписчик')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers',
        verbose_name='На кого подписаны')

    class Meta:
        verbose_name = 'Подписки'
