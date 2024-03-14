from django.db import models
from django.conf import settings
import os

class Pet(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    SIZE_CHOICES = [
        ('miniatura', 'Miniatura'),
        ('pequeno', 'Pequeno'),
        ('médio', 'Médio'),
        ('grande', 'Grande'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age_year = models.IntegerField()
    age_month = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    breed = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    personality = models.JSONField()
    get_along = models.JSONField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)


class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pet_images/')
    order = models.IntegerField(default=0)
    custom_name = models.CharField(max_length=255, blank=True, null=True)

    def delete(self, *args, **kwargs):
        # Remove o arquivo de imagem associado
        if self.image:
            try:
                os.remove(self.image.path)
            except FileNotFoundError:
                pass  # Se o arquivo não existir, não há necessidade de removê-lo

        # Chama o método delete da classe pai para excluir a instância do modelo
        super(PetImage, self).delete(*args, **kwargs)