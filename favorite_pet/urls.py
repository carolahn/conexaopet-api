from django.urls import path
from . import views

urlpatterns = [
    path('add_favorite_pet/<int:pet_id>/', views.add_favorite_pet, name='add_favorite_pet'),
	path('remove_favorite_pet/<int:pet_id>/', views.remove_favorite_pet, name='remove_favorite_pet'),
	path('favorites_pets/<int:user_id>/', views.list_favorite_pets, name='list_favorite_pets_by_user_id'),
]
