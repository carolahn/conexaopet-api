from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'type', 'phone', 'city', 'uf', 'pix', 'image', 'site', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def validate(self, data):
        user_type = data.get('type')

        if user_type == 1:
            required_fields = ['email', 'name', 'username', 'phone', 'city', 'uf', 'password']
        elif user_type == 2:
            required_fields = ['email', 'name', 'username', 'phone', 'city', 'uf', 'password', 'pix', 'image']
        elif user_type == 3:
            required_fields = ['email', 'name', 'username', 'password', 'site', 'image']
        else:
            raise serializers.ValidationError("Invalid user type")

        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is required for user type {user_type}")

        return data