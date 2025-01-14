from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    '''Custom permission to ensure that only the owner of an object can access or modify it.'''
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user