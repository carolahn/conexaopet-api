from rest_framework import viewsets
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

class UpdateUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'user_id'

    def update(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        
        # Obter os dados do request
        data = request.data.copy()
        
        # Verificar se os campos não estão presentes no request e definir como o valor atual do objeto
        if 'name' not in data:
            data['name'] = user.name
        if 'email' not in data:
            data['email'] = user.email
        if 'username' not in data:
            data['username'] = user.username
        if 'phone' not in data:
            data['phone'] = user.phone
        if 'city' not in data:
            data['city'] = user.city
        if 'uf' not in data:
            data['uf'] = user.uf
        if 'pix' not in data:
            data['pix'] = user.pix
        if 'site' not in data:
            data['site'] = user.site
        if 'password' not in data:
            data['password'] = user.password
        
        serializer = self.get_serializer(user, data=data, partial=partial)
        
        if user_id == request.user.id:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({'error': 'You do not have permission to edit this user.'}, status=status.HTTP_403_FORBIDDEN)