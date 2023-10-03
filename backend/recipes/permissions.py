from rest_framework import permissions


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     return (
    #         request.user.is_authenticated
    #         or request.method in permissions.SAFE_METHODS
    #     )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )
