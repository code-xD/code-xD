from rest_framework import permissions,exceptions
from .models import *
import json

class ValidUserAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_X_AUTH')
        if not token:
            return False
        try:
            Profile.objects.get(static_id=token)
        except Profile.DoesNotExist:
            return False
        return True