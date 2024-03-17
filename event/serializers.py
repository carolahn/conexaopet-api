from rest_framework import serializers
from .models import Event, EventImage
from pet.serializers import PetSerializer, PetDescriptionSerializer
from user.serializers import CustomUserSerializer
from address.serializers import AddressSerializer
from pet.models import Pet
import os

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ('id', 'image')

class EventSerializer(serializers.ModelSerializer):
    pets = PetSerializer(many=True, read_only=True)
   
    images = EventImageSerializer(many=True, required=False)
		
    class Meta:
        model = Event
        fields = ['id', 'pets', 'pets_ids', 'date_hour_initial', 'date_hour_end', 'address', 'owner', 'description', 'images', 'is_active', 'is_confirmed', 'followers']
        read_only_fields = ['owner', 'is_active', 'followers']

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('image')
       
        pets_ids_str = validated_data.get('pets_ids', '')
        pets_ids = [int(id) for id in pets_ids_str.split(',') if id.strip()]
     
        event = Event.objects.create(**validated_data)
        
        pets = Pet.objects.filter(pk__in=pets_ids)
        event.pets.set(pets)
        event.pets_ids = pets_ids_str

        for i, image_data in enumerate(images_data):
            event_image = EventImage.objects.create(event=event, image=image_data, order=i)
            image_path = event_image.image.path
            os.chmod(image_path, 0o644)

     
        
        return event

    def update(self, instance, validated_data):
        pets_ids_str = validated_data.get('pets_ids', '')
        new_pets_ids = [int(id) for id in pets_ids_str.split(',') if id.strip()]

        existing_pets_ids = list(instance.pets.values_list('id', flat=True))

        pets_to_remove = set(existing_pets_ids) - set(new_pets_ids)
        instance.pets.remove(*pets_to_remove)

        new_pets = Pet.objects.filter(pk__in=new_pets_ids)
        instance.pets.add(*new_pets)

        instance.date_hour_initial = validated_data.get('date_hour_initial', instance.date_hour_initial)
        instance.date_hour_end = validated_data.get('date_hour_end', instance.date_hour_end)
        instance.address = validated_data.get('address', instance.address)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_confirmed = validated_data.get('is_confirmed', instance.is_confirmed)
        instance.pets_ids = pets_ids_str

        images_data = self.context['request'].FILES.getlist('image')
        
        for image in instance.images.all():
            # Remove fisicamente o arquivo de imagem associado
            if image.image:
                try:
                    os.remove(image.image.path)
                except FileNotFoundError:
                    pass 
            image.delete()
        
        for i, image_data in enumerate(images_data):
            event_image = EventImage.objects.create(event=instance, image=image_data, order=i)
            # Define as permissões do arquivo de imagem após salvá-lo
            image_path = event_image.image.path
            os.chmod(image_path, 0o644)
        
        instance.save()

        return instance
    
class EventDescriptionSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer()
    address = AddressSerializer()
    pets = PetDescriptionSerializer(many=True, read_only=True)
    images = EventImageSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ['id', 'pets', 'pets_ids', 'date_hour_initial', 'date_hour_end', 'address', 'owner', 'description', 'images', 'is_active', 'is_confirmed', 'followers']
        read_only_fields = ['owner', 'is_active', 'followers']
