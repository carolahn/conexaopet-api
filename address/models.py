from django.db import models

class Address(models.Model):
    name = models.CharField(max_length=100, unique=True)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name} - {self.street}, {self.number}, {self.district}, {self.city}, {self.uf}"
