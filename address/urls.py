from django.urls import path
from .views import AddressListCreate, AddressRetrieveUpdateDestroy, AddressList

urlpatterns = [
    path('addresses/', AddressListCreate.as_view(), name='address-list-create'),
    path('addresses/all/', AddressList.as_view(), name='address-list'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDestroy.as_view(), name='address-detail'),
]

