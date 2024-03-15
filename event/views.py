from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, EventImage
from .serializers import EventSerializer, EventImageSerializer
from favorite_event.models import FavoriteEvent
from django.http import Http404
from django.utils import timezone
import json

class EventsPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size' 
    max_page_size = 100  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    if request.user.type != 2:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    request.data['owner'] = request.user.id
    
    serializer = EventSerializer(data=request.data, context={'request': request}) 
    
    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        event = serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'error': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != event.owner:
        return Response({'error': 'You are not the owner of this event'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = EventSerializer(event, data=request.data, partial=True, context={'request': request})
    
    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event_active_status(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'error': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != event.owner:
        return Response({'error': 'You are not the owner of this event'}, status=status.HTTP_403_FORBIDDEN)
    
    is_active = request.data.get('is_active', None)
    if is_active is not None:
        event.is_active = is_active
        event.save()
        return Response({'success': 'Event active status updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'is_active field is required'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_all_events_active_status(request):
    # Verifica se o usuário é autenticado e tem type=2
    if not request.user.is_authenticated or request.user.type != 2:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    # Recupera todos os eventos do usuário autenticado
    events = Event.objects.filter(owner=request.user)
    
    # Atualiza o status de is_active para False em eventos onde date_hour_end passou
    for event in events:
        if event.date_hour_end < timezone.now():
            event.is_active = False
            event.save()

    return Response({'success': 'All events status updated successfully'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def set_event_confirmation(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'error': 'Evento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != event.owner:
        return Response({'error': 'Você não é o proprietário deste evento'}, status=status.HTTP_403_FORBIDDEN)
    
    is_confirmed = request.data.get('is_confirmed', None)

    if is_confirmed is not None:
        event.is_confirmed = is_confirmed
        event.save()

        # Se o evento foi confirmado, envie e-mails aos usuários que o tenham como favorito
        if is_confirmed:
            favorites = FavoriteEvent.objects.filter(event=event)
            for favorite in favorites:
                recipient_email = favorite.user.email
                subject = 'Evento Confirmado'
                message = f'O evento do dia "{event.date_hour_initial}" foi confirmado! Venha participar!'
                sender_email = settings.EMAIL_HOST_USER
                send_mail(subject, message, sender_email, [recipient_email])
                print("email: ", recipient_email)

        return Response({'success': 'Status de confirmação do evento atualizado com sucesso'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'O campo is_confirmed é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_all_events(request):
    events = Event.objects.filter(is_active=True).order_by('date_hour_initial')
    
    paginator = EventsPagination()
    result_page = paginator.paginate_queryset(events, request)

    serializer = EventSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_event_by_id(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404
    
    serializer = EventSerializer(event)
    
    return Response(serializer.data)

