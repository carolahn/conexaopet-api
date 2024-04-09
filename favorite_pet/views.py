from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from .models import FavoritePet
from pet.models import Pet
from pet.serializers import PetDescriptionSerializer 

class FavoritePetPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size' 
    max_page_size = 100 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_pet(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExist:
        return Response({'error': 'Pet com o ID especificado não existe'}, status=status.HTTP_404_NOT_FOUND)

    if FavoritePet.objects.filter(user=request.user, pet=pet).exists():
        return Response({'error': 'Pet já está nos favoritos'}, status=status.HTTP_400_BAD_REQUEST)

    FavoritePet.objects.create(user=request.user, pet=pet)

    # Atualiza o contador de seguidores do evento
    pet.followers = FavoritePet.objects.filter(pet=pet).count()
    pet.save()

    serialized_pet = PetDescriptionSerializer(pet).data

    return Response({'message': 'Pet adicionado aos favoritos com sucesso', 'pet': serialized_pet}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_favorite_pet(request, pet_id):
    try:
        favorite_pet = FavoritePet.objects.get(user=request.user, pet_id=pet_id)
    except FavoritePet.DoesNotExist:
        return JsonResponse({'error': 'Pet favorito não encontrado.'}, status=404)

    # Atualiza o contador de seguidores do pet
    pet = favorite_pet.pet
    favorite_pet.delete()

    pet.followers = FavoritePet.objects.filter(pet=pet).count()
    pet.save()

    serialized_pet = PetDescriptionSerializer(pet).data

    return JsonResponse({'success': 'Pet favorito removido com sucesso.', 'pet': serialized_pet}, status=200)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_favorite_pets(request):
#     try:
#         favorite_pets = FavoritePet.objects.filter(user_id=request.user.id).order_by('-id')
#     except FavoritePet.DoesNotExist:
#         return JsonResponse({'message': 'Não há pets favoritos.'}, status=200)
    
#     paginator = FavoritePetPagination()
#     result_page = paginator.paginate_queryset(favorite_pets, request)

#     serialized_data = [PetDescriptionSerializer(favorite.pet).data for favorite in result_page]
    
#     return paginator.get_paginated_response(serialized_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorite_pets(request):
    try:
        favorite_pets = FavoritePet.objects.filter(user_id=request.user.id).order_by('-id')
    except FavoritePet.DoesNotExist:
        return JsonResponse({'message': 'Não há pets favoritos.'}, status=200)
    
    serialized_data = [PetDescriptionSerializer(favorite.pet).data for favorite in favorite_pets]
    
    return JsonResponse(serialized_data, status=200, safe=False)
        