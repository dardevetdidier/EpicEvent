from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


from django_filters.rest_framework import DjangoFilterBackend
import django_filters.rest_framework
from rest_framework import generics
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
        get_data = request.query_params

        param_sales_contact = get_data.get("sales_contact", None)
        param_status = get_data.get("status", None)

        if param_sales_contact and param_status:
            clients = Client.objects.filter(sales_contact=int(get_data['sales_contact']),
                                            status=get_data['status'])
        elif param_sales_contact:
            clients = Client.objects.filter(sales_contact=int(get_data['sales_contact']))
        elif param_status:
            clients = Client.objects.filter(status=get_data['status'])

        else:
            clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(data=self.request.data)

        # Check permission
        if self.request.user.has_perm('crm.add_client'):
            if serializer.is_valid():
                for client in clients:
                    if serializer.validated_data["email"] == client.email:
                        return Response("Client already exists")


                try:
                    sales_member = SalesTeamMember.objects.filter(employee__exact=self.request.user)[0]
                except IndexError:
                    return Response("Can't create a Client. There're no sales team members in database")
                serializer.save()
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


class ContractList(generics.ListAPIView):
    """List of all contracts. Can be filtered by 'sales_contact', 'client' or 'signed_status'"""
    permission_classes = [IsAuthenticated]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sales_contact', 'client', 'signed_status']


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
        get_data = self.request.query_params
        print(get_data)
        param_support_contact = get_data.get("support_contact", None)
        param_event_status = get_data.get("event_status", None)
        if param_support_contact and param_event_status:
            events = Event.objects.filter(support_contact_id=int(param_support_contact),
                                          event_status_id=int(param_event_status))
        elif param_support_contact:
            events = Event.objects.filter(support_contact_id=int(param_support_contact))
        elif param_event_status:
            events = Event.objects.filter(event_status_id=int(param_event_status))
        else:
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
        print(event.client.sales_contact.employee)
        print(self.request.user)
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
                serializer.validated_data["sales_contact"] = client.sales_contact
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
        if self.request.user.has_perm('crm.add_event') and self.request.user == client.sales_contact.employee:
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
