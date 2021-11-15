from django.contrib import admin
from .models import ManagementTeamMember, SalesTeamMember, SupportTeamMember, Client, Contract, EventStatus, Event

admin.site.register(ManagementTeamMember)
admin.site.register(SalesTeamMember)
admin.site.register(SupportTeamMember)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(EventStatus)
admin.site.register(Event)
