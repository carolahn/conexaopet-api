from django.urls import path
from .views import CreateUserView
from .views import CustomUserViewSet, CreateUserView, UpdateUserView, ProtectorUserListView
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/update/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),
    path('users/protector/', ProtectorUserListView.as_view(), name='protector_user-list'),
]