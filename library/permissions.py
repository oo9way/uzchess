from rest_framework.permissions import BasePermission, IsAdminUser


class DefaultMethodsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        elif request.method == "POST":
            return IsAdminUser().has_permission(request, view)

        else:
            return False


class IsOwnerOfObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
