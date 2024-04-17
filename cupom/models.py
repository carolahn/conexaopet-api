from django.db import models
from django.conf import settings

class Cupom(models.Model):
    value = models.CharField(max_length=100, null=True)
    expiration = models.DateTimeField()
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='cupom_images/', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cupom'