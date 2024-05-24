"""Классы пермишенов для управления доступом к данным в зависимости от роли."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    message = 'Пользователь должен быть администратором'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsOwnerOrAdmin(BasePermission):
    message = 'Пользователь должен быть администратором или создателем'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.owner == request.user
            or request.user.is_admin
        )


class IsAuthorAdminSuperuserModeratorOrReadOnly(BasePermission):
    message = 'Пользователь должен быть администратором, модератором или автор'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class IsAdminOrReadOnly(BasePermission):
    message = (
        'Проверка пользователя является ли он администратором '
        'или автором объекта, иначе только режим чтения'
    )

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_admin
        )
