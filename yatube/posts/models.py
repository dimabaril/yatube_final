from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Group model."""
    title = models.CharField(max_length=200, verbose_name="Группа")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="slug")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Группы"


class Post(models.Model):
    """Post model."""
    text = models.TextField(
        verbose_name="Текст",
        help_text="Текст нового поста",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор"
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name="Группа",
        help_text="Группа, к которой будет относиться пост",
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "Посты"


class Comment(models.Model):
    """Comment model."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Комментарий",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор"
    )
    text = models.TextField(
        verbose_name="Текст",
        help_text="Текст комментария",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время публикации"
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-created']
        verbose_name_plural = "Комметарии"


class Follow(models.Model):
    """Who on who is subscribed. User subscribed on author."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name_plural = "Подписки"


class Like(models.Model):
    """Likes for posts."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Like",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Автор"
    )

    class Meta:
        verbose_name_plural = "Likes"
