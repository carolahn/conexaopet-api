from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from .models import FavoriteEvent
from event.models import Event 
from event.serializers import EventDescriptionSerializer  

class FavoriteEventPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size' 
    max_page_size = 100 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Evento com o ID especificado não existe'}, status=status.HTTP_404_NOT_FOUND)
    
    if FavoriteEvent.objects.filter(user=request.user, event=event).exists():
        return Response({'error': 'Evento já está nos favoritos'}, status=status.HTTP_400_BAD_REQUEST)
    
    FavoriteEvent.objects.create(user=request.user, event=event)
    
    # Atualiza o contador de seguidores do evento
    event.followers = FavoriteEvent.objects.filter(event=event).count()
    event.save()

    serialized_event = EventDescriptionSerializer(event).data
    
    return Response({'message': 'Evento adicionado aos favoritos com sucesso', 'event': serialized_event}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_favorite_event(request, event_id):
    try:
        favorite_event = FavoriteEvent.objects.get(user=request.user, event_id=event_id)
    except FavoriteEvent.DoesNotExist:
        return JsonResponse({'error': 'Evento favorito não encontrado.'}, status=404)

    # Atualiza o contador de seguidores do evento
    event = favorite_event.event
    favorite_event.delete()

    event.followers = FavoriteEvent.objects.filter(event=event).count()
    event.save()

    serialized_event = EventDescriptionSerializer(event).data

    return JsonResponse({'success': 'Evento removido dos favoritos com sucesso.', 'event': serialized_event}, status=200)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_favorite_events(request):
#     try:
#         favorite_events = FavoriteEvent.objects.filter(user_id=request.user.id).order_by('-id')
#     except FavoriteEvent.DoesNotExist:
#         return JsonResponse({'error': 'Não há eventos favoritos.'}, status=404)

#     paginator = FavoriteEventPagination()
#     result_page = paginator.paginate_queryset(favorite_events, request)

#     serialized_data = [EventDescriptionSerializer(favorite.event).data for favorite in result_page]

#     return paginator.get_paginated_response(serialized_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorite_events(request):
    try:
        favorite_events = FavoriteEvent.objects.filter(user_id=request.user.id).order_by('-id')
    except FavoriteEvent.DoesNotExist:
        return JsonResponse({'error': 'Não há eventos favoritos.'}, status=404)

    serialized_data = [EventDescriptionSerializer(favorite.event).data for favorite in favorite_events]

    return JsonResponse(serialized_data, status=200, safe=False)

