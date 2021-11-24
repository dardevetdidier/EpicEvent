from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm.models import Client, Contract, Event, EventStatus, SalesTeamMember
from crm.serializers import ClientSerializer, ContractSerializer, EventSerializer, EventStatusSerializer
from crm.permissions import \
    ClientSalesTeamAllSupportTeamRead, \
    ContractSalesTeamAllSupportTeamRead, \
    EventSalesTeamAllSupportTeamsReadCreateUpdate, \
    EventStatusSalesAndSupportTeamAll


def get_object(element, pk):
    """Get the object wich matches with the model and the id"

    :param element:
        model
    :param pk:
        int: id of the object
    :return:
        objet which matches with pk
    """
    try:
        return element.objects.get(pk=pk)
    except element.DoesNotExist:
        raise Http404


class ClientList(APIView):
    """List of all clients, or create a new client """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClientSerializer(data=self.request.data)
        # Check permission
        if self.request.user.has_perm('crm.add_client'):
            if serializer.is_valid():
                serializer.save()
                sales_member = SalesTeamMember.objects.filter(employee__exact=self.request.user)[0]
                serializer.validated_data["sales_contact"] = sales_member
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied


class ClientDetail(APIView):
    """Retrieve, update and delete a client instance"""
    permission_classes = [IsAuthenticated, ClientSalesTeamAllSupportTeamRead]

    def get(self, request, pk):
        client = get_object(Client, pk)
        self.check_object_permissions(request, obj=client)
        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        client = get_object(Client, pk)
        self.check_object_permissions(request, obj=client)
        serializer = ClientSerializer(client, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contracts = Contract.objects.all()
        client = get_object(Client, pk)
        self.check_object_permissions(request, obj=client)
        for contract in contracts:
            if client == contract.client:
                return Response(status=status.HTTP_403_FORBIDDEN)

        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractList(APIView):
    """List of all contracts, or create a new contract"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContractDetail(APIView):
    """Retrieve, update or delete a contract instance"""
    permission_classes = [IsAuthenticated, ContractSalesTeamAllSupportTeamRead]

    def get(self, request, pk):
        contract = get_object(Contract, pk)
        self.check_object_permissions(request, obj=contract)
        serializer = ContractSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        contract = get_object(Contract, pk)
        self.check_object_permissions(request, obj=contract)
        serializer = ContractSerializer(contract, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contract = get_object(Contract, pk)
        self.check_object_permissions(request, obj=contract)
        contract.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventList(APIView):
    """List of all events"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDetail(APIView):
    """Retrieve, update or delete an event instance"""
    permission_classes = [IsAuthenticated, EventSalesTeamAllSupportTeamsReadCreateUpdate]

    def get(self, request, pk):
        event = get_object(Event, pk)
        self.check_object_permissions(request, obj=event)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        event = get_object(Event, pk)
        self.check_object_permissions(request, obj=event)
        serializer = EventSerializer(event, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = get_object(Event, pk)
        self.check_object_permissions(request, obj=event)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractsClientList(APIView):
    """List of contracts related to a client, or create a contract for a client"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        client = get_object(Client, pk)
        contracts = Contract.objects.filter(client_id=client.pk)
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        client = get_object(Client, pk)
        serializer = ContractSerializer(data=self.request.data)
        if self.request.user.has_perm('crm.add_contract') and self.request.user == client.sales_contact.employee:
            if serializer.is_valid():
                serializer.validated_data["client"] = client
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied


class EventsClientList(APIView):
    """List of events related to a client, or create an event for a client"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        client = get_object(Client, pk)
        events = Event.objects.filter(client_id=client.pk)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        client = get_object(Client, pk)
        serializer = EventSerializer(data=request.data)
        if self.request.user.has_perm('crm.add_event') and self.request.user == client.saless_contact.employee:
            if serializer.is_valid():
                serializer.validated_data["client"] = client
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied


class EventStatusList(APIView):
    """List of event status, or create an event status"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        event_status = EventStatus.objects.all()
        serializer = EventStatusSerializer(event_status, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EventStatusSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventStatusDetail(APIView):
    """Retrieve, update or delete an event status"""
    permission_classes = [IsAuthenticated, EventStatusSalesAndSupportTeamAll]

    def get(self, request, pk):
        event_status = get_object(EventStatus, pk)
        self.check_object_permissions(request, obj=event_status)
        serializer = EventStatusSerializer(event_status)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        event_status = get_object(EventStatus, pk)
        self.check_object_permissions(request, obj=event_status)
        serializer = EventStatusSerializer(event_status, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event_status = get_object(EventStatus, pk)
        self.check_object_permissions(request, obj=event_status)
        event_status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
