import rest_framework.permissions
from rest_framework.permissions import BasePermission

from my_user.user_manager import Role


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        is_admin = request.user.role == Role.ADMIN.__str__()
        return bool(request.user.is_authenticated and is_admin)


class IsUser(BasePermission):

    def has_permission(self, request, view):
        is_user = request.user.role == Role.USER.__str__()
        return bool(request.user.is_authenticated and is_user)


class AllowAny(rest_framework.permissions.AllowAny):
    def has_permission(self, request, view):
        return True


