from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (obj.author_id == getattr(request.user, 'id', None) or request.user.is_staff)
        )

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, "owner_id"):
            return obj.owner_id == request.user.id or request.user.is_staff

        if hasattr(obj, "list") and hasattr(obj.list, "owner_id"):
            return obj.list.owner_id == request.user.id or request.user.is_staff

        return False