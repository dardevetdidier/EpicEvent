from django.http import Http404
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crm.models import Client, Contract
from crm.serializers import ClientSerializer, ContractSerializer


def get_object(element, pk):
    try:
        return element.objects.get(pk=pk)
    except element.DoesNotExist:
        raise Http404


class ClientList(APIView):
    """List of all clients, or create a new client """
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClientSerializer(data=self.request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetail(APIView):
    """Retrieve, update and delete a client instance"""

    def get(self, request, pk):
        client = get_object(Client, pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        client = get_object(Client, pk)
        serializer = ClientSerializer(client, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = get_object(Client, pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractList(APIView):
    """List of all contracts, or create a new contract"""
    def get(self, request):
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContractSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractDetail(APIView):
    """Retrieve, update or delete a contract instance"""

    def get(self, request, pk):
        contract = get_object(Contract, pk)
        serializer = ContractSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        contract = get_object(Contract, pk)
        serializer = ContractSerializer(contract, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contract = get_object(Contract, pk)
        contract.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

