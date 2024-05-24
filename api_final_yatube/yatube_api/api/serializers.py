from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.

    Позволяет преобразовывать объекты Post в JSON и обратно.
    """

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'pub_date', 'id',)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Позволяет преобразовывать объекты Comment в JSON и обратно.
    """

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'author', 'created', 'post')


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.

    Позволяет преобразовывать объекты Group в JSON и обратно.
    """

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Follow.

    Позволяет преобразовывать объекты Follow в JSON и обратно.
    """

    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        """Не разрешает пользователю подписаться на самого себя."""
        user = self.context.get('request').user
        following = data['following']

        if user == following:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя.'
            )

        return data
