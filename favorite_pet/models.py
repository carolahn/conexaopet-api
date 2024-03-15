from django.db import models
from django.conf import settings
from pet.models import Pet

class FavoritePet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pet')

    def __str__(self):
        return f'{self.user.username} - {self.pet.name}'
