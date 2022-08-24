"""
Custom permissions
"""
from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """
    Object-level permission to only allow user to edit is profile
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
