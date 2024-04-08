from django.urls import path
from .views import create_event, update_event, get_all_events, get_event_by_id, update_event_active_status, set_event_confirmation, update_all_events_active_status, search_event, EventListByProtector, delete_event

urlpatterns = [
    path('events/', create_event, name='create_event'),
    path('events/update/<int:pk>/', update_event, name='update_event'),
    path('events/update-all/', update_all_events_active_status, name='update_all_events_active_status'),
	path('events/update/is_active/<int:pk>/', update_event_active_status, name='update_event_active_status'),
	path('events/update/is_confirmed/<int:pk>/', set_event_confirmation, name='set_event_confirmation'),
    path('events/all/', get_all_events, name='get_all_events'),
    path('events/<int:pk>/', get_event_by_id, name='event-detail'),
    path('events/search/', search_event, name='search-event'),
    path('events/protector/<int:pk>/', EventListByProtector.as_view(), name='event-list-by-protector'),
    path('events/delete/<int:pk>/', delete_event, name='delete_event'),
]
