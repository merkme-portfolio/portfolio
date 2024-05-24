"""Модели приложения Блог."""
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


# Получаем модель пользователя
User = get_user_model()


class PostInfo(models.Model):
    """Абстрактная модель для хранения общей информации о публикации."""

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        """Указываем на абстрактность класса."""

        abstract = True

    def __str__(self):
        """Возращаем читаемое название заголовкам."""
        return self.title


class Post(PostInfo):
    """Модель для хранения информации о публикации."""

    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        'Location',
        verbose_name='Местоположение',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL
    )

    image = models.ImageField(
        'Фото',
        upload_to='posts_images',
        blank=True
    )

    class Meta:
        """Задаем вывод в обратном порядке по полю дата и время публикации."""

        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        """При обращении к модели возвращаем ссылку."""
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Category(PostInfo):
    """Модель для хранения информации о категории публикации."""

    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        ),
        unique=True
    )

    class Meta:
        """Русифицируем."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(models.Model):
    """Модель для хранения информации о местоположении публикации."""

    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название места'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        """Русифицируем."""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        """Возращаем читаемые названия местам."""
        return self.name


class Comment(models.Model):
    """Модель для хранения комментариев."""

    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время комментария'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Сортировка комментариев по дате и времени комментария."""

        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Возращаем читаемое название для текста публикации."""
        return self.text
