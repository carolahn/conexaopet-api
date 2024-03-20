from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'member'),
        (2, 'protector'),
        (3, 'sponsor'),
    )
    type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True) 
    uf = models.CharField(max_length=3, blank=True, null=True) 
    pix = models.CharField(max_length=100, blank=True, null=True) 
    site = models.CharField(max_length=100, blank=True, null=True) 
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    is_staff = models.BooleanField(blank=True, null=True, default=False)
    is_superuser = models.BooleanField(blank=True, null=True, default=False)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    date_joined = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'custom_user'

