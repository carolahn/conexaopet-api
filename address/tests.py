from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Address
from .serializers import AddressSerializer

class AddressModelTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            name='Casa',
            street='Rua Principal',
            number='123',
            district='Centro',
            city='Cidade',
            uf='UF'
        )

    def test_address_str(self):
        self.assertEqual(str(self.address), 'Casa - Rua Principal, 123, Centro, Cidade, UF')


class AddressSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'name': 'Casa',
            'street': 'Rua Principal',
            'number': '123',
            'district': 'Centro',
            'city': 'Cidade',
            'uf': 'UF'
        }

    def test_valid_data(self):
        serializer = AddressSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = ''  # name vazio deve ser inválido
        serializer = AddressSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class AddressAPITest(APITestCase):
    def setUp(self):
        self.address = Address.objects.create(
            name='Casa',
            street='Rua Principal',
            number='123',
            district='Centro',
            city='Cidade',
            uf='UF'
        )

    def test_address_list(self):
        url = reverse('address-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_address_create(self):
        url = reverse('address-list-create')
        data = {
            'name': 'Trabalho',
            'street': 'Rua Trabalho',
            'number': '456',
            'district': 'Bairro',
            'city': 'Cidade',
            'uf': 'UF'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_address_detail(self):
        url = reverse('address-detail', kwargs={'pk': self.address.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)