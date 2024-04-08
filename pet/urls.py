from django.urls import path
from .views import create_pet, update_pet, get_all_pets, get_pet_by_id, update_pet_active_status, search_pet, get_pets_by_protector, delete_pet, PetsByProtectorListView

urlpatterns = [
    path('pets/', create_pet, name='create_pet'),
    path('pets/update/<int:pk>/', update_pet, name='update_pet'),
    path('pets/update/is_active/<int:pk>/', update_pet_active_status, name='update_pet_active_status'),
    path('pets/all/', get_all_pets, name='get_all_pets'),
    path('pets/<int:pk>/', get_pet_by_id, name='pet-detail'),
    path('pets/search/', search_pet, name='search-pet'),
    path('pets/protector/<int:pk>/', get_pets_by_protector, name='get_pets_by_protector'),
    path('pets/delete/<int:pk>/', delete_pet, name='delete_pet'),
    path('pets/protector/<int:pk>/all/', PetsByProtectorListView.as_view(), name='pets_by_protector_list'),
]