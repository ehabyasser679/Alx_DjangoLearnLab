from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow safe (read-only) access to everyone.
    Write access is only granted to the author of the object.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
