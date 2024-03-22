from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            type=1,
            phone='123456789',
            city='City',
            uf='UF',
            pix='testpix',
            site='www.example.com',
            name='Test User'
        )

    def test_user_creation(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        saved_user = CustomUser.objects.get(username='testuser')
        self.assertEqual(saved_user.username, 'testuser')
        self.assertEqual(saved_user.email, 'test@example.com')
        self.assertEqual(saved_user.type, 1)

class CustomUserSerializerTest(TestCase):
    def test_valid_data(self):
        serializer = CustomUserSerializer(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'type': 1,
            'phone': '123456789',
            'city': 'City',
            'uf': 'UF',
            'pix': 'testpix',
            'site': 'www.example.com',
            'name': 'Test User'
        })
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        serializer = CustomUserSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'username', 'password'})
        
class CustomUserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            type=1,
            phone='123456789',
            city='City',
            uf='UF',
            pix='testpix',
            site='www.example.com',
            name='Test User'
        )

    def test_register_view(self):
        url = reverse('register')
        response = self.client.post(url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'type': 1,
            'phone': '987654321',
            'city': 'New City',
            'uf': 'NY',
            'pix': 'newpix',
            'site': 'www.newexample.com',
            'name': 'New User'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_token_obtain_view(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)