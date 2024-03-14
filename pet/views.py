from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Pet, PetImage
from .serializers import PetSerializer, PetImageSerializer

class PetsPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size' 
    max_page_size = 100 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_pet(request):
    if request.user.type != 2:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    request.data['owner'] = request.user.id
    serializer = PetSerializer(data=request.data, context={'request': request}) 
    
    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        pet = serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_pets(request):
    # Recupera todos os pets ativos do banco de dados
    pets = Pet.objects.filter(is_active=True)
    
    paginator = PetsPagination()
    result_page = paginator.paginate_queryset(pets, request)

    # Serializa os pets para formatar a resposta
    serializer = PetSerializer(result_page, many=True)
    
    # Retorna a lista de pets
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_pet_by_id(request, pk):
    try:
        # Recupera o pet pelo ID
        pet = Pet.objects.get(pk=pk, is_active=True)
    except Pet.DoesNotExist:
        # Se o pet não existir ou não estiver ativo, retorna um erro 404
        raise Http404
    
    # Serializa o pet para formatar a resposta
    serializer = PetSerializer(pet)
    
    # Retorna os detalhes do pet
    return Response(serializer.data)