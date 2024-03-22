from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FavoritePet
from user.models import CustomUser
from pet.models import Pet

class FavoritePetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword', type=2)
        self.pet = Pet.objects.create(
            name='Simba', gender='M', age_year=2, age_month=0, weight='12.0',
            size='médio', breed=5, owner=self.user,
            description='Curious and playful cat', is_active=True, type=2, followers=0
        )
        self.client.force_authenticate(user=self.user)

    def test_add_favorite_pet(self):
        url = reverse('add_favorite_pet', kwargs={'pet_id': self.pet.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FavoritePet.objects.filter(user=self.user, pet=self.pet).exists())

    def test_remove_favorite_pet(self):
        FavoritePet.objects.create(user=self.user, pet=self.pet)
        url = reverse('remove_favorite_pet', kwargs={'pet_id': self.pet.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(FavoritePet.objects.filter(user=self.user, pet=self.pet).exists())

    def test_list_favorite_pets(self):
        FavoritePet.objects.create(user=self.user, pet=self.pet)
        url = reverse('list_favorite_pets_by_user_id')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Simba')