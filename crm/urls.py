from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.ClientList.as_view(), name="clients"),
    path('clients/<int:pk>/', views.ClientDetail.as_view(), name="client-detail"),
    path('contracts/', views.ContractList.as_view(), name="contracts"),
    path('contracts/<int:pk>/', views.ContractDetail.as_view(), name="contract-detail"),
    path('events/', views.EventList.as_view(), name='events'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),
]
