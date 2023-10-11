from rest_framework import permissions

class IsAdminRole(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return request.user.role == 1

class IsUserRole(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return request.user.role in [1, 2]

class IsRestaurantRole(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return request.user.role in [1, 3]

class IsRiderRole(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return request.user.role in [1, 4]

