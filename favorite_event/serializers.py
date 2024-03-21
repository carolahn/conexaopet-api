from rest_framework import serializers
from .models import FavoriteEvent

class FavoriteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteEvent
        fields = []
