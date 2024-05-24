from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from posts.models import Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    API-представление для взаимодействия с моделью Post.

    Позволяет просматривать, создавать, обновлять и удалять посты.

    Только авторизованные пользователи могут создавать,
    обновлять и удалять посты.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Сохраняет автора поста как текущего пользователя."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API-представление для взаимодействия с моделью Comment.

    Позволяет просматривать, создавать, обновлять и удалять
    комментарии к постам.

    Только авторизованные пользователи могут создавать,
    обновлять и удалять комментарии.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API-представление для просмотра групп.

    Позволяет только просматривать группы.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    API-представление для взаимодействия с моделью Follow.

    Позволяет просматривать, создавать, обновлять
    и удалять подписки на пользователей.

    Только авторизованные пользователи могут создавать,
    обновлять и удалять подписки.
    Поддерживает поиск по имени пользователя.
    """

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
