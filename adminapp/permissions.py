from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Allows access only to admin users (superusers).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role== 'staff'

class IsLibrarian(BasePermission):
    """
    Custom permission to allow only librarians to add books.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'librarian'