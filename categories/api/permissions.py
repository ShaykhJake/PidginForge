from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
        # elif request.user.is_staff != True:
        #     return False


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
        # elif request.user.is_staff != True:
        #     return False
