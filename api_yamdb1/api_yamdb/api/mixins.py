from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrReadOnly


class CreateDestroyListViewSetMixin(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet, который обеспечивает создание, удаление.

    И получение списка объектов.
    """


class CategoryGenreMixin:
    """
    Миксин для представлений категорий и жанров.

    Включает настройки пагинации, разрешения, фильтрацию и поиск.
    """
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
