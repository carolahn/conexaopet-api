from rest_framework import serializers
from .models import Pet, PetImage
from user.serializers import CustomUserSerializer
from user.models import CustomUser
import os

class PetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetImage
        fields = ('id', 'image')

class PetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, required=False)

    class Meta:
        model = Pet
        fields = ['id', 'name', 'gender', 'age_year', 'age_month', 'weight', 'size', 'breed', 'owner', 'personality', 'get_along', 'description', 'images', 'is_active', 'type', 'followers']
        read_only_fields = ['owner', 'is_active', 'followers']

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('image')
        pet = Pet.objects.create(**validated_data)
        for i, image_data in enumerate(images_data):
            pet_image = PetImage.objects.create(pet=pet, image=image_data, order_number=i)
            # Define as permissões do arquivo de imagem após salvá-lo
            image_path = pet_image.image.path
            os.chmod(image_path, 0o644)
        return pet

    def update(self, instance, validated_data):
      
        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age_year = validated_data.get('age_year', instance.age_year)
        instance.age_month = validated_data.get('age_month', instance.age_month)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.size = validated_data.get('size', instance.size)
        instance.breed = validated_data.get('breed', instance.breed)
        instance.personality = validated_data.get('personality', instance.personality)
        instance.get_along = validated_data.get('get_along', instance.get_along)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)

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
            pet_image = PetImage.objects.create(pet=instance, image=image_data, order_number=i)
            # Define as permissões do arquivo de imagem após salvá-lo
            image_path = pet_image.image.path
            os.chmod(image_path, 0o644)
        
        instance.save()

        return instance
    
class PetDescriptionSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer()
    images = PetImageSerializer(many=True, required=False)

    class Meta:
        model = Pet
        fields = ['id', 'name', 'gender', 'age_year', 'age_month', 'weight', 'size', 'breed', 'owner', 'personality', 'get_along', 'description', 'images', 'is_active', 'type', 'followers']
        read_only_fields = ['owner', 'is_active']

class SearchPetSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=Pet.TYPE_CHOICES, required=False)
    city = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=Pet.GENDER_CHOICES, required=False)
    age = serializers.ChoiceField(choices=Pet.STAGE_LIFE_CHOICES, required=False)
    size = serializers.ChoiceField(choices=Pet.SIZE_CHOICES, required=False)
    breed = serializers.ChoiceField(choices=Pet.BREED_CHOICES, required=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    personality = serializers.CharField(required=False)
    get_along = serializers.CharField(required=False)