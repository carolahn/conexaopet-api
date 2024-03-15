from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import FavoritePet
from pet.models import Pet
from pet.serializers import PetSerializer 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_pet(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id)
        FavoritePet.objects.create(user=request.user, pet=pet)
        return Response({'message': 'Pet adicionado aos favoritos com sucesso'}, status=status.HTTP_201_CREATED)
    except Pet.DoesNotExist:
        return Response({'error': 'Pet com o ID especificado não existe'}, status=status.HTTP_404_NOT_FOUND)

def remove_favorite_pet(request, pet_id):
    try:
        favorite_pet = FavoritePet.objects.get(user=request.user, pet_id=pet_id)
    except FavoritePet.DoesNotExist:
        return JsonResponse({'error': 'Pet favorito não encontrado.'}, status=404)

    favorite_pet.delete()

    return JsonResponse({'success': 'Pet favorito removido com sucesso.'}, status=200)

def list_favorite_pets(request, user_id):
    try:
        favorite_pets = FavoritePet.objects.filter(user_id=user_id)
    except FavoritePet.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)

    serialized_data = [PetSerializer(favorite.pet).data for favorite in favorite_pets]

    return JsonResponse(serialized_data, safe=False, status=200)