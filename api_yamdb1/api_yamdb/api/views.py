from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .permissions import (
    IsAdmin, IsOwnerOrAdmin,
    IsAuthorAdminSuperuserModeratorOrReadOnly, IsAdminOrReadOnly
)
from .serializers import (
    SignUpSerializer, TokenSerializer, UserSerializer,
    CommentSerializer, ReviewSerializer, GenreSerializer,
    TitleSerializer, CategorySerializer
)
from .filters import TitleFilter
from .utils import (
    check_confirmation_code, generate_confirmation_code,
    send_confirmation_email
)
from .mixins import CreateDestroyListViewSetMixin, CategoryGenreMixin
from reviews.models import Category, Genre, Review, Title
from users.models import User


class SignUpView(APIView):
    """Регистрация нового пользователя."""

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Создает нового пользователя.

        Отправляет код подтверждения на email.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data
            )
        except IntegrityError:
            return Response(
                'Такой логин или email уже существуют',
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            confirmation_code = generate_confirmation_code(user)
            send_confirmation_email(user, confirmation_code)
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )


class TokenView(APIView):
    """Получение токена для аутентификации."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Проверяет код подтверждения и возвращает токен, если код верен."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        if check_confirmation_code(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
            )
        return Response(
            'Неверный код подтверждения',
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Управление пользователями (CRUD операции)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    search_fields = ['username']
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated, IsOwnerOrAdmin]
    )
    def me(self, request):
        """Получение и обновление собственного профиля пользователя."""
        if request.method == 'PATCH':
            serializer = SignUpSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            if 'role' in serializer.validated_data:
                serializer.validated_data.pop('role')
            serializer.save()
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )

        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Читать отзывы может любой пользователь.

    Опубликовать озыв о произведении, авторизованный пользователь.
    Редактировать и удалять публикации, автор публикации.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminSuperuserModeratorOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """
    Оставить комментарий на отзыв сможет авторизованный пользователь.

    Редактировать и удалить комментарий, автор комментария.
    """

    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorAdminSuperuserModeratorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )


class GenreViewSet(CategoryGenreMixin, CreateDestroyListViewSetMixin):
    """
    Получить список жанров сможет любой пользователь.

    Добавить и удалить жанр, админ.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CategoryGenreMixin, CreateDestroyListViewSetMixin):
    """
    Получить список всех категорий сможет любой пользователь.

    Создать категорию может только админ.
    Поле slug каждой категории должно быть уникальным.
    Удалить категорию может только админ.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить произведение или список произведений сможет любой пользователь.

    Редактировать, добавить и удалить произведение, админ.
    """

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
