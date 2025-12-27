"""
Custom permissions for role-based access control.
"""

from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """Permission check for student role."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsInstructor(permissions.BasePermission):
    """Permission check for instructor role."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_instructor


class IsAdmin(permissions.BasePermission):
    """Permission check for admin role."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin_user


class IsInstructorOrAdmin(permissions.BasePermission):
    """Permission check for instructor or admin role."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_instructor or request.user.is_admin_user
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission check for object owner or admin."""
    
    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.is_admin_user:
            return True
        
        # Check if object has a user attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object is the user itself
        if hasattr(obj, 'id') and hasattr(request.user, 'id'):
            return obj.id == request.user.id
        
        return False
