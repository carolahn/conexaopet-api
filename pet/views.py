from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail
from django.conf import settings
from .models import Pet
from .serializers import PetSerializer, PetDescriptionSerializer, SearchPetSerializer
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from favorite_pet.models import FavoritePet
from django.http import Http404

class PetsPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size' 
    max_page_size = 100 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_pet(request):
    if request.user.type != 2:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    request_data = request.data.copy()
    request_data['owner'] = request.user.id
    serializer = PetSerializer(data=request_data, context={'request': request}) 
    
    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        serializer.save()

        created_pet = Pet.objects.get(pk=serializer.data['id'])
        created_serializer = PetDescriptionSerializer(created_pet)
        
        return Response(created_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_pet(request, pk):
    try:
        pet = Pet.objects.get(pk=pk)
    except Pet.DoesNotExist:
        return Response({'error': 'Pet does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != pet.owner:
        return Response({'error': 'You are not the owner of this pet'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = PetSerializer(pet, data=request.data, partial=True, context={'request': request})
    
    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        serializer.save()

        # Envie e-mails aos usuários que favoritaram o pet
        favorites = FavoritePet.objects.filter(pet=pet)
        for favorite in favorites:
            recipient_email = favorite.user.email
            subject = 'Atualização de Pet'
            message = f'Olá,\n\nO pet "{pet.name}" foi atualizado. Confira as novidades!'
            sender_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender_email, [recipient_email])

        updated_pet = Pet.objects.get(pk=serializer.data['id'])
        updated_serializer = PetDescriptionSerializer(updated_pet)

        return Response(updated_serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_pets(request):
    pets = Pet.objects.filter(is_active=True).order_by('-id')
    
    paginator = PetsPagination()
    result_page = paginator.paginate_queryset(pets, request)

    serializer = PetSerializer(result_page, many=True)
    
    for pet_data in serializer.data:   
        owner_id = pet_data.get('owner')
        try:
            owner_instance = CustomUser.objects.get(pk=owner_id)
            owner_data = CustomUserSerializer(owner_instance).data
            pet_data['owner'] = owner_data 
        except CustomUser.DoesNotExist:
            pass  

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_pet_by_id(request, pk):
    try:
        pet = Pet.objects.get(pk=pk)
    except Pet.DoesNotExist:
        raise Http404
    
    serializer = PetDescriptionSerializer(pet)
    
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_pet_active_status(request, pk):
    try:
        pet = Pet.objects.get(pk=pk)
    except Pet.DoesNotExist:
        return Response({'error': 'Pet does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != pet.owner:
        return Response({'error': 'You are not the owner of this pet'}, status=status.HTTP_403_FORBIDDEN)
    
    is_active = request.data.get('is_active', None)
    if is_active is not None:
        pet.is_active = is_active
        pet.save()

        if is_active is False:
            # Envie e-mails aos usuários que favoritaram o pet
            favorites = FavoritePet.objects.filter(pet=pet)
            for favorite in favorites:
                recipient_email = favorite.user.email
                subject = 'Pet indisponível'
                message = f'Olá,\n\nO pet "{pet.name}" não está mais disponível.\nVeja outros pets que estão aguardando um lar.'
                sender_email = settings.EMAIL_HOST_USER
                send_mail(subject, message, sender_email, [recipient_email])

            favorites.delete()

        return Response({'success': 'Pet active status updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'is_active field is required'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def search_pet(request):
    serializer = SearchPetSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    
    city = data.get('city')
    if city:
        owners = CustomUser.objects.filter(type=2, city__icontains=city)
        pets = Pet.objects.filter(is_active=True, owner__in=owners).order_by('-id')
    else:
        pets = Pet.objects.filter(is_active=True).order_by('-id')

    if 'name' in data:
        pets = pets.filter(name__icontains=data['name'])
    if 'type' in data:
        pets = pets.filter(type=data['type'])
    if 'gender' in data:
        pets = pets.filter(gender=data['gender'])
    if 'age' in data:
        age = data['age']
        if age == 1:
            pets = pets.filter(age_year=0)
        elif age == 2:
            pets = pets.filter(age_year__gt=0, age_year__lt=10)
        else:
            pets = pets.filter(age_year__gte=10)
    if 'size' in data:
        pets = pets.filter(size=data['size'])
    if 'breed' in data:
        pets = pets.filter(breed=data['breed'])
    if 'owner' in data:
        pets = pets.filter(owner=data['owner'])
    if 'personality' in data:
        personality_values = [int(personality) for personality in data['personality'].split(',')]
        pets = pets.filter(personality__overlap=personality_values)
    if 'get_along' in data:
        get_along_values = [int(get_along) for get_along in data['get_along'].split(',')]
        pets = pets.filter(get_along__overlap=get_along_values)

    paginator = PetsPagination()
    result_page = paginator.paginate_queryset(pets, request)
    
    serializer = PetDescriptionSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)