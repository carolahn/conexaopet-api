from rest_framework import viewsets
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
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

         # Se uma nova imagem for enviada, exclua a imagem anterior do usuário
        if 'image' in data:
            user.image.delete(save=False) 
        
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

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            username = request.data.get('username') 

            try:
                custom_user = CustomUser.objects.get(username=username)
                custom_data = {
                    'user_id': custom_user.id,
                    'username': custom_user.username,
                    'email': custom_user.email,
                    'type': custom_user.type,
                    'phone': custom_user.phone,
                    'city': custom_user.city,
                    'uf': custom_user.uf,
                    'pix': custom_user.pix,
                    'site': custom_user.site,
                    'name': custom_user.name,
                    'image': custom_user.image.url if custom_user.image else None
                }
                response.data['user'] = custom_data
 
            except CustomUser.DoesNotExist:
                pass
           
        return response