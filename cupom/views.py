from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import Cupom
from .serializers import CupomSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_cupom(request):
    # Verifica se o usuário autenticado é do tipo 3
    if request.user.type != 3:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    # Define o usuário autenticado como o proprietário do cupom
    request.data['owner'] = request.user.id
    
    # Cria o serializador com os dados fornecidos na requisição
    serializer = CupomSerializer(data=request.data)
    
    # Verifica se os dados são válidos
    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        # Salva o cupom no banco de dados
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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
    
    # Cria o serializador com os dados fornecidos na requisição
    serializer = CupomSerializer(cupom, data=request.data)
    
    # Verifica se os dados são válidos
    if serializer.is_valid():
        # Salva as atualizações do cupom no banco de dados
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_cupons(request):
    # Recupera todos os cupons ativos do banco de dados
    cupons = Cupom.objects.filter(is_active=True)
    
    # Serializa os cupons para formatar a resposta
    serializer = CupomSerializer(cupons, many=True)
    
    # Retorna a lista de cupons
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])  # Permite acesso sem autenticação
def get_cupom_by_id(request, pk):
    try:
        # Recupera o cupom pelo ID
        cupom = Cupom.objects.get(pk=pk, is_active=True)
    except Cupom.DoesNotExist:
        # Se o cupom não existir ou não estiver ativo, retorna um erro 404
        raise Http404
    
    # Serializa o cupom para formatar a resposta
    serializer = CupomSerializer(cupom)
    
    # Retorna os detalhes do cupom
    return Response(serializer.data)
