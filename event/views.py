from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .models import Event
from .serializers import EventSerializer, EventDescriptionSerializer
from favorite_event.models import FavoriteEvent
from django.http import Http404
from django.utils import timezone
from django.db.models import Q
from address.models import Address
import os


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
    
    try:
        address_id = request.data.get('address')
        address_instance = Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        return Response({'error': 'Invalid address ID.'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        serializer.validated_data['address'] = address_instance

        serializer.save()

        created_event = Event.objects.get(pk=serializer.data['id'])
        created_serializer = EventDescriptionSerializer(created_event)
        
        return Response(created_serializer.data, status=status.HTTP_201_CREATED)
    
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
    
    try:
        address_id = request.data.get('address', event.address.id)
        address_instance = Address.objects.get(pk=address_id)
    except Address.DoesNotExist:
        return Response({'error': 'Invalid address ID.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        serializer.validated_data['address'] = address_instance

        serializer.save()

        updated_event = Event.objects.get(pk=serializer.data['id'])
        updated_serializer = EventDescriptionSerializer(updated_event)

        return Response(updated_serializer.data, status=status.HTTP_200_OK)
    
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
    if not request.user.is_authenticated or request.user.type != 2:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    events = Event.objects.filter(owner=request.user)
    
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

        return Response({'success': 'Status de confirmação do evento atualizado com sucesso'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'O campo is_confirmed é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_all_events(request):
    events = Event.objects.filter(is_active=True).order_by('date_hour_initial')
    
    paginator = EventsPagination()
    result_page = paginator.paginate_queryset(events, request)

    serializer = EventDescriptionSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_event_by_id(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404
    
    serializer = EventDescriptionSerializer(event)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_event(request):
    pets_names = request.query_params.get('pets', None)
    date = request.query_params.get('date', None)
    city = request.query_params.get('city', None)
    owner_id = request.query_params.get('owner', None)

    events = Event.objects.filter(is_active=True).order_by('-id')

    if pets_names:
        pets = pets_names.split(',')
        # Q objects para criar condições OR para cada nome de pet
        pet_filters = Q()
        for pet_name in pets:
            pet_filters |= Q(pets__name__icontains=pet_name.strip())
        events = events.filter(pet_filters)

    if date:
        events = events.filter(date_hour_initial__date=date)

    if city:
        addresses = Address.objects.filter(city__icontains=city)
        events = events.filter(address__in=addresses)

    if owner_id:
        events = events.filter(owner_id=owner_id)

    paginator = EventsPagination()
    result_page = paginator.paginate_queryset(events, request)

    serializer = EventDescriptionSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


class EventListByProtector(APIView):
    def get(self, request, pk):
        try:
            events = Event.objects.filter(owner_id=pk, is_active=True).order_by('-id')

            paginator = EventsPagination()
            result_page = paginator.paginate_queryset(events, request)

            serializer = EventDescriptionSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)
        except Event.DoesNotExist:
            return Response({'error': 'Events not found for the specified protector ID.'}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({'error': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if request.user != event.owner:
        return Response({'error': 'You are not the owner of this event'}, status=status.HTTP_403_FORBIDDEN)

    # Remove as imagens associadas ao event
    for image in event.images.all():
        if image.image:
            try:
                os.remove(image.image.path)
            except FileNotFoundError:
                pass
        image.delete()

    # Remove as entradas de favorite_event relacionadas ao event
    favorites = FavoriteEvent.objects.filter(event=event)
    for favorite in favorites:
        recipient_email = favorite.user.email
        subject = 'Evento cancelado'
        message = f'Olá,\n\nO evento de "{event.owner.username}" em "{event.address.name}" foi cancelado.\nVeja outros eventos de adoção em ConexãoPet.'
        sender_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, sender_email, [recipient_email])
    favorites.delete()

    event.delete()

    return Response({'success': 'Event deleted successfully'}, status=status.HTTP_200_OK)