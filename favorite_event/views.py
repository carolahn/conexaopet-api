from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import FavoriteEvent
from event.models import Event 
from event.serializers import EventSerializer  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        FavoriteEvent.objects.create(user=request.user, event=event)
        return Response({'message': 'Evento adicionado aos favoritos com sucesso'}, status=status.HTTP_201_CREATED)
    except Event.DoesNotExist:
        return Response({'error': 'Evento com o ID especificado não existe'}, status=status.HTTP_404_NOT_FOUND)

def remove_favorite_event(request, event_id):
    try:
        favorite_event = FavoriteEvent.objects.get(user=request.user, event_id=event_id)
    except FavoriteEvent.DoesNotExist:
        return JsonResponse({'error': 'Evento favorito não encontrado.'}, status=404)

    favorite_event.delete()

    return JsonResponse({'success': 'Evento favorito removido com sucesso.'}, status=200)

def list_favorite_events(request, user_id):
    try:
        favorite_events = FavoriteEvent.objects.filter(user_id=user_id)
    except FavoriteEvent.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)

    serialized_data = [EventSerializer(favorite.event).data for favorite in favorite_events]

    return JsonResponse(serialized_data, safe=False, status=200)

