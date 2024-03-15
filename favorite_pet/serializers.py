from rest_framework import serializers
from .models import FavoritePet

class FavoritePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritePet
        fields = []