from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, SalesTeamMember, SupportTeamMember, ManagementTeamMember, EventStatus, Event, Contract


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class SalesTeamMemberSerializer(serializers.ModelSerializer):
    employee = UserSerializer(many=True, read_only=True)

    class Meta:
        model = SalesTeamMember
        fields = "__all__"


class ManagementTeamMemberSerializer(serializers.ModelSerializer):
    employee = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ManagementTeamMember
        fields = "__all__"


class SupportTeamMemberSerializer(serializers.ModelSerializer):
    employee = UserSerializer(many=True, read_only=True)

    class Meta:
        model = SupportTeamMember
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    sales_contact = SalesTeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = "__all__"


class EventStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventStatus
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=True, read_only=True)
    support_contact = SupportTeamMemberSerializer(many=True, read_only=True)
    event_status = EventStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    sales_contact = SalesTeamMemberSerializer(many=True, read_only=True)
    client = ClientSerializer(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = "__all__"
