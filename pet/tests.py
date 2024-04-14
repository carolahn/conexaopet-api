from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from user.models import CustomUser
from .models import Pet
from django.core.files.uploadedfile import SimpleUploadedFile

class PetTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword', type=2)
        self.client.login(username='testuser', password='testpassword')

    def test_create_pet(self):
        url = reverse('create_pet')
        data = {
            'name': 'Buddy',
            'gender': 'M',
            'age_year': 2,
            'age_month': 6,
            'weight': '15.5',
            'breed': 1,
            'owner': self.user.id,
            'personality[]': 4,
            'personality[]': 9,
            'get_along[]': 1,
            'get_along[]': 2,
            'description': 'Friendly and energetic dog',
            'is_active': True,
            'type': 1,
            'followers': 0
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Buddy')

def test_update_pet(self):
    pet = Pet.objects.create(
        name='Max', gender='M', age_year=3, age_month=0, weight=20,
        breed=2, owner=self.user,
        description='Playful and friendly', is_active=True, type=1, followers=0
    )
    url = reverse('update_pet', kwargs={'pk': pet.pk})
    data = {
        'name': 'Maximus',
        'weight': '22.0',
        'description': 'Loves playing fetch and going for walks'
    }
    
    uploaded_file = SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain")
    multipart_data = {
        'name': data['name'],
        'weight': data['weight'],
        'description': data['description'],
        'file_field_name': uploaded_file,  # Se houver campos de arquivo, adicione-os aqui
    }
    response = self.client.put(url, multipart_data, format='multipart', content_type='multipart/form-data')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], 'Maximus')
    self.assertEqual(response.data['weight'], '22.00')

    def test_get_all_pets(self):
        url = reverse('get_all_pets')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pet_by_id(self):
        pet = Pet.objects.create(
            name='Luna', gender='F', age_year=1, age_month=6, weight='10.5',
            size='pequeno', breed=3, owner=self.user,
            description='Sweet and affectionate', is_active=True, type=2, followers=0
        )
        url = reverse('pet-detail', kwargs={'pk': pet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Luna')

    def test_update_pet_active_status(self):
        pet = Pet.objects.create(
            name='Rocky', gender='M', age_year=4, age_month=0, weight='25.0',
            size='grande', breed=4, owner=self.user,
            description='Gentle giant', is_active=True, type=1, followers=0
        )
        url = reverse('update_pet_active_status', kwargs={'pk': pet.pk})
        data = {'is_active': False}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], 'Pet active status updated successfully')

    def test_search_pet(self):
        Pet.objects.create(
            name='Simba', gender='M', age_year=2, age_month=0, weight='12.0',
            size='médio', breed=5, owner=self.user,
            description='Curious and playful cat', is_active=True, type=2, followers=0
        )
        url = reverse('search-pet')
        data = {'name': 'Simba', 'type': 2}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'Simba')
