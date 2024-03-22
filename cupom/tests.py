from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import Cupom
from user.models import CustomUser
from .serializers import CupomSerializer
from django.utils import timezone

class CupomModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', type=3)
        self.cupom = Cupom.objects.create(
            value='10%',
            expiration=timezone.now(),
            description='Test Cupom',
            owner=self.user
        )

    def test_cupom_creation(self):
        self.assertEqual(Cupom.objects.count(), 1)
        saved_cupom = Cupom.objects.get(value='10%')
        self.assertEqual(saved_cupom.value, '10%')
        self.assertEqual(saved_cupom.description, 'Test Cupom')
        self.assertEqual(saved_cupom.owner, self.user)

class CupomSerializerTest(TestCase):
    def test_valid_data(self):
        user_data = {
			'username': 'testuser',
			'email': 'test@example.com',
			'password': 'testpassword',
			'type': 1,
			'phone': '123456789',
			'city': 'City',
			'uf': 'UF',
			'pix': 'testpix',
			'image': None,
			'site': 'www.example.com',
			'name': 'Test User'
   		}
        serializer = CupomSerializer(data={
			'value': '20%',
			'expiration': '2024-03-25T10:00:00Z',
			'description': 'Test Cupom',
			'owner': user_data,
			'is_active': True
		})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_data(self):
        serializer = CupomSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'owner'})

class CupomViewsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword', type=3)
        self.client.login(username='testuser', password='testpassword')

    def test_create_cupom_view(self):
        url = reverse('create_cupom')
        response = self.client.post(url, {
            'value': '30%',
            'expiration': '2024-03-25T10:00:00Z',
            'description': 'Test Cupom',
            'owner': self.user.id,
            'is_active': True
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cupom.objects.count(), 1)

    def test_update_cupom_view(self):
        cupom = Cupom.objects.create(
            value='40%',
            expiration='2024-03-25T10:00:00Z',
            description='Test Cupom',
            owner=self.user
        )
        url = reverse('update_cupom', kwargs={'pk': cupom.pk})
        response = self.client.put(url, {
            'value': '50%',
            'expiration': '2024-03-26T10:00:00Z',
            'description': 'Updated Test Cupom'
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cupom.objects.get(pk=cupom.pk).value, '50%')