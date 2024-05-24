from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

from .validators import validate_username_not_me
from reviews.constants import USER_MAX_LEN_BIO, USER_MAX_LEN_ROLE


class UserRole(models.TextChoices):
    """Роли пользователей."""

    USER = 'user', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    """Модель для пользователей."""

    username_validators = [
        UnicodeUsernameValidator(),
        validate_username_not_me
    ]

    default_field_length = 150
    default_email_length = 254

    username = models.CharField(
        max_length=default_field_length,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
        validators=username_validators,
    )
    email = models.EmailField(
        max_length=default_email_length,
        verbose_name='E-mail',
        help_text='Укажите e-mail',
        unique=True,
    )
    first_name = models.CharField(
        max_length=default_field_length,
        verbose_name='Имя',
        help_text='Укажите ваше имя',
        blank=True,
    )
    last_name = models.CharField(
        max_length=default_field_length,
        verbose_name='Фамилия',
        help_text='Укажите вашу фамилию',
        blank=True,
    )
    bio = models.TextField(
        max_length=USER_MAX_LEN_BIO,
        verbose_name='О себе',
        help_text='Расскажите о себе',
        blank=True,
    )
    role = models.CharField(
        max_length=USER_MAX_LEN_ROLE,
        verbose_name='Роль',
        help_text='Права доступа',
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.role == UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    def __str__(self):
        return self.username
