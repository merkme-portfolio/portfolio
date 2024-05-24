"""Настройка фильтрации для полей."""
import django_filters

from reviews.models import Category, Genre, Title


class TitleFilter(django_filters.FilterSet):
    """Фильтр объектов модели Title."""

    name = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter()
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        to_field_name='slug'
    )
    genre = django_filters.ModelChoiceFilter(
        field_name='genre',
        queryset=Genre.objects.all(),
        to_field_name='slug'
    )

    class Meta:
        """Метаданные для фильтрации модели Title."""

        model = Title
        fields = ['category', 'genre', 'name', 'year']
