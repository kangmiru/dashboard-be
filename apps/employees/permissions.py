from rest_framework import permissions

class NotLoggedIn(permissions.IsAuthenticated):
    """
    User belum terdaftar
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
class MySelf(permissions.IsAuthenticated):
    """
    Hanya dapat melihat
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj
    
class AnyBody(permissions.AllowAny):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS