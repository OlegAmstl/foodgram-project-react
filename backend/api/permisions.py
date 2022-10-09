from rest_framework.permissions import (BasePermission,
                                        IsAuthenticatedOrReadOnly)


class AdminOrReadOnly(BasePermission):
    """Разрешение на создание и изменение только для админов.
    Остальным только чтение объекта."""

    def has_permission(self, request, view):
        return (
                request.method in ('GET',)
                or request.user.is_authenticated
                and request.user.is_admin
        )
