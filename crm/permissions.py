from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import Client


class ClientSalesTeamAllSupportTeamRead(permissions.BasePermission):
    """
    Client Permissions.
    view level: Checks if user is authenticated.
    object level: Sales Team member is allowed to make all CRUD operations
                  Support team memeber is allowed to Read
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):

        if request.method == 'GET' and request.user.has_perm('crm.view_client'):
            return True

        if request.method == 'PUT' and request.user.has_perm('crm.change_client') \
                and request.user == obj.sales_contact.employee:
            return True

        if request.method == 'DELETE' and request.user.has_perm('crm.delete_client'):
            return True

        return False


class ContractSalesTeamAllSupportTeamRead(permissions.BasePermission):
    """
    Contract Permissions.
    view level: Checks if user is authenticated.
    object level: Sales Team member is allowed to make all CRUD operations
                  Support team memeber is allowed to Read
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' and request.user.has_perm('crm.view_contract'):
            return True

        if request.method == 'PUT' and request.user.has_perm('crm.change_contract') \
                and request.user == obj.sales_contact.employee:
            return True

        if request.method == 'DELETE' and request.user.has_perm('crm.delete_contract') \
                and request.user == obj.sales_contact.employee:
            return True

        return False
