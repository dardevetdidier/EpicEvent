from django.utils import timezone
from rest_framework import permissions


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
                  Support team member is allowed to Read
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


class EventSalesTeamAllSupportTeamsReadCreateUpdate(permissions.BasePermission):
    """
    Event Permissions.
    view level: Checks if user is authenticated.
    object level: Sales team member is allowed to make all CRUD operations
                  Support Team member is allowed to read, create and update an event

    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' and request.user.has_perm('crm.view_event'):
            return True

        if request.method == 'PUT' and request.user.has_perm('crm.change_event') \
                and (request.user == obj.client.sales_contact.employee
                     or
                     (request.user == obj.support_contact.employee and obj.event_date >= timezone.now())):
            return True

        if request.method == 'DELETE' and request.user.groups.filter(name="Sales team") \
                and request.user == obj.client.sales_contact.employee:
            return True

        return False


class EventStatusSalesAndSupportTeamAll(permissions.BasePermission):
    """
        EventStatus Permissions.
        view level: Checks if user is authenticated.
        object level: Sales and Support team members are allowed to make all CRUD operations

    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' and (request.user.groups.filter(name="Sales team") or
                                        request.user.groups.filter(name="Support team")):
            return True

        if request.method == 'PUT' and (request.user.groups.filter(name="Sales team") or
                                        request.user.groups.filter(name="Support team")):
            return True

        if request.method == 'DELETE' and (request.user.groups.filter(name="Sales team") or
                                           request.user.groups.filter(name="Support team")):
            return True

        return False
