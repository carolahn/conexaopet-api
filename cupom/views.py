from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from datetime import timedelta
from .models import Cupom
from .serializers import CupomSerializer, CupomUpdateSerializer
from django.http import QueryDict

class CupomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_cupom(request):
    if request.user.type != 3:
        return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
    
    # request_data = request.data
    request_data = QueryDict('', mutable=True)
    request_data.update(request.data)
    request_data['owner'] = request.user.id

    serializer = CupomUpdateSerializer(data=request_data)
    
    if serializer.is_valid():
        serializer.validated_data['owner'] = request.user
        
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
    
    if request.user != cupom.owner:
        return Response({'error': 'You are not the owner of this cupom'}, status=status.HTTP_403_FORBIDDEN)
    
    request_data = request.data;
    request_data['owner'] = request.user.id

    serializer = CupomUpdateSerializer(cupom, data=request_data)
    
    if serializer.is_valid():
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
    
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])  
def get_cupom_by_id(request, pk):
    try:
        cupom = Cupom.objects.get(pk=pk)
    except Cupom.DoesNotExist:
        raise Http404
    
    serializer = CupomSerializer(cupom)
 
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def update_expired_cupons(request):
    user = request.user
    
    # Cupons que já estão inativos
    inactive_cupons = Cupom.objects.filter(owner=user, is_active=False)
    inactive_count = inactive_cupons.count()
    for cupom in inactive_cupons:
        if cupom.image:
            cupom.image.delete()
        cupom.delete()

    # Cupons que expiraram
    expired_cupons = Cupom.objects.filter(owner=user, expiration__lt=timezone.now())
    expired_count = expired_cupons.count()
    deleted_count = inactive_count + expired_count
    for cupom in expired_cupons:
        cupom.is_active = False
        cupom.save()

    # Envia a nova lista de cupons ativos
    cupons = Cupom.objects.filter(owner=user, is_active=True).order_by('expiration')

    paginator = CupomPagination()
    result_page = paginator.paginate_queryset(cupons, request)
    
    serializer = CupomSerializer(result_page, many=True)

    response_data = {
        'cupons': serializer.data,
        'deleted_count': deleted_count,
    }
    
    return paginator.get_paginated_response(response_data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_coupons(request):
#     user = request.user
#     paginator = CupomPagination()

#     user_coupons = Cupom.objects.filter(owner=user).order_by('expiration')
#     result_page = paginator.paginate_queryset(user_coupons, request)

#     serializer = CupomSerializer(result_page, many=True)
    
#     return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_coupons(request, pk):
    paginator = CupomPagination()

    user_coupons = Cupom.objects.filter(owner_id=pk).order_by('expiration')
    result_page = paginator.paginate_queryset(user_coupons, request)

    serializer = CupomSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cupom(request, pk):
    try:
        cupom = Cupom.objects.get(pk=pk)
    except Cupom.DoesNotExist:
        return Response({'error': 'Cupom does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != cupom.owner:
        return Response({'error': 'You are not the owner of this cupom'}, status=status.HTTP_403_FORBIDDEN)
    
    # Remover a imagem associada ao cupom se existir
    if cupom.image:
        cupom.image.delete()

    cupom.delete()
    
    return Response({'success': 'Cupom deleted successfully'}, status=status.HTTP_204_NO_CONTENT)