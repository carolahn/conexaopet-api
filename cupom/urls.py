from django.urls import path
from .views import create_cupom, update_cupom, get_all_cupons, get_cupom_by_id

urlpatterns = [
    path('cupons/', create_cupom, name='create_cupom'),
    path('cupons/update/<int:pk>/', update_cupom, name='update_cupom'),
    path('cupons/<int:pk>/', get_cupom_by_id, name='cupom-detail'),
    path('cupons/all/', get_all_cupons, name='get_all_cupons'),
]

