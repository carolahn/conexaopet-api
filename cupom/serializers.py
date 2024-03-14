from rest_framework import serializers
from .models import Cupom

class CupomSerializer(serializers.ModelSerializer):
    expiration = serializers.DateTimeField(required=False)
    
    class Meta:
        model = Cupom
        fields = ['id', 'value', 'expiration', 'image', 'owner', 'is_active']
        read_only_fields = ['owner', 'is_active']