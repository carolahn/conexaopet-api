from django.urls import path
from . import views

urlpatterns = [
    path('add_favorite_event/<int:event_id>/', views.add_favorite_event, name='add_favorite_event'),
    path('remove_favorite_event/<int:event_id>/', views.remove_favorite_event, name='remove_favorite_event'),
    path('favorite_events/', views.list_favorite_events, name='list_favorite_events_by_user_id'),
]
