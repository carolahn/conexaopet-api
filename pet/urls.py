from django.urls import path
from .views import create_pet, update_pet, get_all_pets, get_pet_by_id, update_pet_active_status, search_pet

urlpatterns = [
    path('pets/', create_pet, name='create_pet'),
    path('pets/update/<int:pk>/', update_pet, name='update_pet'),
    path('pets/update/is_active/<int:pk>/', update_pet_active_status, name='update_pet_active_status'),
    path('pets/all/', get_all_pets, name='get_all_pets'),
    path('pets/<int:pk>/', get_pet_by_id, name='pet-detail'),
    path('pets/search/', search_pet, name='search-pet'),
]