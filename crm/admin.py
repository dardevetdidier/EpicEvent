from django.contrib import admin

from .models import ManagementTeamMember, SalesTeamMember, SupportTeamMember, Client, Contract, EventStatus, Event


class UserAdmin(admin.ModelAdmin):
    list_display = ['last name', 'first_name', 'username', 'email']


# @admin.register(SalesTeamMember)
# class SalesTeamAdmin(admin.ModelAdmin):
#     list_display = ['id', 'employee', 'date_created']
#
#
# @admin.register(SupportTeamMember)
# class SupportTeamAdmin(admin.ModelAdmin):
#     list_display = ['id', 'employee', 'date_created']
#
#
# @admin.register(ManagementTeamMember)
# class ManagementTeamAdmin(admin.ModelAdmin):
#     list_display = ['id', 'employee', 'date_created']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "last_name",
        "first_name",
        "email",
        "phone",
        "mobile",
        "company_name",
        "sales_contact",
    ]
    search_fields = ["last_name", ]
    list_per_page = 10


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "sales_contact",
        "client",
        "date_created",
        "date_updated",
        "amount",
        "payment_due",
    ]
    list_per_page = 10

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client",
        "date_created",
        "date_updated",
        "support_contact",
        "event_status",
        "attendees",
        "event_date",
        "notes",
    ]

    list_editable = [
        "support_contact",
        "event_status",
        "attendees",
        "event_date",
        "notes",
        ]
    list_per_page = 10


admin.site.register(ManagementTeamMember)
admin.site.register(SalesTeamMember)
admin.site.register(SupportTeamMember)
# admin.site.register(Client)
# admin.site.register(Contract)
admin.site.register(EventStatus)
# admin.site.register(Event)
