"""Админ панель."""
from django.contrib import admin
from .models import Category, Location, Post, Comment


class PostInline(admin.TabularInline):
    """Добавляем отображение модели публикация в виде TabularInline."""

    model = Post
    extra = 0


class CommentInline(admin.StackedInline):
    """Добавляем комментарии под публикациями в виде StackedInline."""

    model = Comment
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    """Добавляем отображение публикаций под относящейся к ней категории."""

    inlines = (
        PostInline,
    )


class LocationAdmin(admin.ModelAdmin):
    """Добавляем отображение публикаций под относящейся к ней локации."""

    inlines = (
        PostInline,
    )


class PostAdmin(admin.ModelAdmin):
    """Расширенная панель для Публикаций."""

    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'location',
        'category',
        'is_published'
    )

    inlines = (
        CommentInline,
    )

    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
