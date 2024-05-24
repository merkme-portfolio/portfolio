from django.contrib import admin
from .models import Category, Genre, Title, Review, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административный класс для модели Категория."""

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Административный класс для модели Жанр."""

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Административный класс для модели Произведение."""

    list_display = ('name', 'year', 'category')
    list_filter = ('category', 'genre')
    search_fields = ('name', 'year', 'category__name')
    filter_horizontal = ('genre',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Административный класс для модели Отзыв."""

    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('title__name', 'author__username')
    ordering = ('-pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Административный класс для модели Комментарий."""

    list_display = ('review', 'author', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('review__title__name', 'author__username')
    ordering = ('-pub_date',)
