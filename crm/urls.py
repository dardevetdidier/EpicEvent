from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.ClientList.as_view(), name="clients"),
    path('clients/<int:pk>/', views.ClientDetail.as_view(), name="client-detail"),
    path('clients/<int:pk>/contracts/', views.ContractsClientList.as_view(), name='contracts-client'),
    path('clients/<int:pk>/events/', views.EventsClientList.as_view(), name='events-client'),
    path('contracts/', views.ContractList.as_view(), name="contracts"),
    path('contracts/<int:pk>/', views.ContractDetail.as_view(), name="contract-detail"),
    path('events/', views.EventList.as_view(), name='events'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
]
