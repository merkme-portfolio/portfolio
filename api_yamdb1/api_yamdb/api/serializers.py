from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]


class SignUpSerializer(UserSerializer):
    """Сериализатор для регистрации, включает валидацию username и email."""

    username = serializers.CharField(
        max_length=User.default_field_length,
        validators=User.username_validators
    )
    email = serializers.EmailField(
        max_length=User.default_email_length
    )


class TokenSerializer(serializers.ModelSerializer):
    """
    Сериализатор для аутентификации по токену.

    Включает в себя валидацию username и код подтверждения.
    """

    username = serializers.CharField(
        max_length=User.default_field_length,
        validators=User.username_validators
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ['id', 'author', 'text', 'pub_date', 'score']

    def validate(self, data):
        """Проверяет, оставлял ли пользователь уже отзыв о произведении."""
        title_id = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        method = self.context['request'].method

        if method == 'POST' and Review.objects.filter(
            author=author, title_id=title_id
        ).exists():
            raise ValidationError(
                'Вы уже оставляли отзыв на это произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'pub_date']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    lookup_field = 'slug'

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    lookup_field = 'slug'

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = [
            'id', 'rating', 'name', 'year', 'description', 'genre', 'category'
        ]

    def get_rating(self, obj):
        """Вычисляет средний рейтинг произведения на основе отзывов."""
        reviews = obj.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('score'))['score__avg']
        return None

    def to_representation(self, instance):
        """Представляет данные о произведении с учетом связанных объектов."""
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['genre'] = GenreSerializer(
            instance.genre.all(), many=True
        ).data
        return representation
