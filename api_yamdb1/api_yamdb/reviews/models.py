from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_current_year
from .constants import ModelDefaultSettings, TEXT_SHOWS_ON_PAGE


class Category(models.Model):
    """Модель для категорий произведений."""

    name = models.TextField(
        max_length=ModelDefaultSettings.NAME_LENGTH,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        max_length=ModelDefaultSettings.SLUG_LENGTH,
        verbose_name='Slug категории',
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return (
            f'{self.name[:TEXT_SHOWS_ON_PAGE]} | '
            f'{self.slug[:TEXT_SHOWS_ON_PAGE]} '
        )


class Genre(models.Model):
    """Модель для жанров произведений."""

    name = models.TextField(
        max_length=ModelDefaultSettings.NAME_LENGTH,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        max_length=ModelDefaultSettings.SLUG_LENGTH,
        verbose_name='Slug жанра',
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return (
            f'{self.name[:TEXT_SHOWS_ON_PAGE]} | '
            f'{self.slug[:TEXT_SHOWS_ON_PAGE]} '
        )


class Title(models.Model):
    """Модель для произведений."""

    name = models.TextField(
        max_length=ModelDefaultSettings.NAME_LENGTH,
        verbose_name='Название',
    )
    year = models.PositiveIntegerField(
        validators=[validate_current_year],
        help_text='Для указания года выпуска используйте формат: <YYYY>',
        verbose_name='Год выпуска',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория', related_name='title',
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр',
        blank=True,
        through='GenreTitle',
    )
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание'
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return (
            f'Title: {self.name[:TEXT_SHOWS_ON_PAGE]} | {self.year} '
            f'Category: {self.category} | Genre: {self.genre}'
        )


class GenreTitle(models.Model):
    """Промежуточная модель для связи жанров и произведений."""

    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связи жанра и произведений'

    def __str__(self):
        return f'Связь: {self.genre.name} - {self.title.name}'


class Review(models.Model):
    """Модель для отзывов о произведениях."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Заголовок', related_name='reviews',
    )
    text = models.TextField(verbose_name='Текст отзыва',)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='reviews',
    )
    score = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ['author', 'title']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return (
            f'Text rewiev: {self.text[:TEXT_SHOWS_ON_PAGE]} | '
            f'{self.pub_date} | Author: {self.author.username} '
            f'| Title: {self.title} | Score: {self.score}'
        )


class Comment(models.Model):
    """Модель для комментариев к отзывам."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='комментарий', related_name='comments',
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Автор',
        on_delete=models.CASCADE, related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария', auto_now_add=True, db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (
            f'Author: {self.author.username} | Review: {self.review} | '
            f'Text comment: {self.text[:TEXT_SHOWS_ON_PAGE]} | {self.pub_date}'
        )
