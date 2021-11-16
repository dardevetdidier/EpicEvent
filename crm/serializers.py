from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, SalesTeamMember, SupportTeamMember, ManagementTeamMember, EventStatus, Event, Contract


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class SalesTeamMemberSerializer(serializers.ModelSerializer):
    employee = UserSerializer()

    class Meta:
        model = SalesTeamMember
        fields = "__all__"


class ManagementTeamMemberSerializer(serializers.ModelSerializer):
    employee = UserSerializer()

    class Meta:
        model = ManagementTeamMember
        fields = "__all__"


class SupportTeamMemberSerializer(serializers.ModelSerializer):
    employee = UserSerializer()

    class Meta:
        model = SupportTeamMember
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    # sales_contact = SalesTeamMemberSerializer()

    class Meta:
        model = Client
        fields = "__all__"


class EventStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStatus
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    support_contact = SupportTeamMemberSerializer()
    event_status = EventStatusSerializer()

    class Meta:
        model = Event
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    sales_contact = SalesTeamMemberSerializer()
    client = ClientSerializer()

    class Meta:
        model = Contract
        fields = "__all__"
