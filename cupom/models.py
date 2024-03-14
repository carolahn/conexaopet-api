from django.db import models
from django.conf import settings

class Cupom(models.Model):
    value = models.CharField(max_length=100)
    expiration = models.DateTimeField()
    image = models.ImageField(upload_to='cupom_images/', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
