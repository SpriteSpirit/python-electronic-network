from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    """
    Разрешение для проверки, является ли пользователь активным.
    """

    def has_permission(self, request, view):
        # Проверка, что пользователь аутентифицирован и активен
        return request.user.is_authenticated and request.user.is_active
