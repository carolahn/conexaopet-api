from django.urls import path
from .views import AddressListCreate, AddressRetrieveUpdateDestroy

urlpatterns = [
    path('addresses/', AddressListCreate.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDestroy.as_view(), name='address-detail'),
]
