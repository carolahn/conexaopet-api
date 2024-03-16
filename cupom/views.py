from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from .models import Cupom
from .serializers import CupomSerializer, CupomUpdateSerializer

class CupomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_cupom(request):
    # Verifica se o usuário autenticado é do tipo 3
    if request.user.type != 3:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    # Define o usuário autenticado como o proprietário do cupom
    request.data['owner'] = request.user.id
    
    # Cria o serializador com os dados fornecidos na requisição
    serializer = CupomUpdateSerializer(data=request.data)
    
    # Verifica se os dados são válidos
    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        # Salva o cupom no banco de dados
        serializer.save()

        created_cupom = Cupom.objects.get(pk=serializer.data['id'])
        created_serializer = CupomSerializer(created_cupom)
      
        return Response(created_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cupom(request, pk):
    try:
        cupom = Cupom.objects.get(pk=pk)
    except Cupom.DoesNotExist:
        return Response({'error': 'Cupom does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Verifica se o usuário autenticado é o proprietário do cupom
    if request.user != cupom.owner:
        return Response({'error': 'You are not the owner of this cupom'}, status=status.HTTP_403_FORBIDDEN)
    
    request.data['owner'] = request.user.id

    # Cria o serializador com os dados fornecidos na requisição
    serializer = CupomUpdateSerializer(cupom, data=request.data)
    
    # Verifica se os dados são válidos
    if serializer.is_valid():
        # Salva as atualizações do cupom no banco de dados
        serializer.save()

        updated_cupom = Cupom.objects.get(pk=pk)
        updated_serializer = CupomSerializer(updated_cupom)

        return Response(updated_serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_cupons(request):
    cupons = Cupom.objects.filter(is_active=True).order_by('expiration')
    
    paginator = CupomPagination()
    result_page = paginator.paginate_queryset(cupons, request)
    
    serializer = CupomSerializer(result_page, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])  # Permite acesso sem autenticação
def get_cupom_by_id(request, pk):
    try:
        # Recupera o cupom pelo ID
        cupom = Cupom.objects.get(pk=pk)
    except Cupom.DoesNotExist:
        # Se o cupom não existir ou não estiver ativo, retorna um erro 404
        raise Http404
    
    # Serializa o cupom para formatar a resposta
    serializer = CupomSerializer(cupom)
    
    # Retorna os detalhes do cupom
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def update_expired_cupons(request):
    user = request.user
    # Busca todos os cupons do usuário que ainda estão ativos
    active_cupons = Cupom.objects.filter(owner=user, is_active=True)
    
    expired_count = 0

    # Itera sobre os cupons para verificar e atualizar conforme necessário
    for cupom in active_cupons:
        # Verifica se a data de expiração já passou
        if cupom.expiration < timezone.now():
            # Define is_active como False
            cupom.is_active = False
            cupom.save()
            expired_count += 1
    
    # Retorna uma resposta vazia, pois a atualização foi feita com sucesso
    return Response({'Cupons expirados': expired_count}, status=status.HTTP_200_OK)