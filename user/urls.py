from django.urls import path
from .views import CreateUserView
from .views import CustomUserViewSet, CreateUserView, UpdateUserView

urlpatterns = [
    path('users/', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/update/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),
]