from rest_framework import permissions
from .models import Client


class ClientSalesTeamAllSupportTeamRead(permissions.BasePermission):
    """
    Client Permissions.
    view level: Checks if user is authenticated.
    object level: Sales Team emeber is allowed to make all CRUD operations
                  Support team memeber is allowed to Read
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.has_perm('crm.view_client'):
            return True
