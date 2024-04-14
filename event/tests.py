from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from copy import deepcopy
from .models import Event
from user.models import CustomUser
from address.models import Address
from pet.models import Pet 

class EventTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword', type=2)
        self.address = Address.objects.create(city='Test City', street='Test Street', number='123')
        self.client.force_authenticate(user=self.user)
        self.pet = Pet.objects.create(name='Test Pet', type=1, gender='M', age_year=2, age_month=6, weight=10.5, size='Small', breed=1, owner=self.user, description='Test description')

    def test_create_event(self):
        url = reverse('create_event')
        data = {
            'date_hour_initial': '2024-03-25T08:00:00Z',
            'date_hour_end': '2024-03-25T12:00:00Z',
            'address': self.address.id,
            'description': 'Test Event',
            'is_active': True,
            'is_confirmed': False,
            'followers': 0,
            'pet[]': self.pet.id
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_event(self):
        event = Event.objects.create(owner=self.user, date_hour_initial='2024-03-25T08:00:00Z', date_hour_end='2024-03-25T12:00:00Z', address=self.address, description='Test Event')
        url = reverse('update_event', kwargs={'pk': event.pk})
        data = {
            'date_hour_initial': '2024-03-25T10:00:00Z',
            'date_hour_end': '2024-03-25T14:00:00Z',
            'description': 'Updated Event Description'
        }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_event = Event.objects.get(pk=event.pk)
        self.assertEqual(updated_event.date_hour_initial.strftime('%Y-%m-%dT%H:%M:%SZ'), '2024-03-25T10:00:00Z')
        self.assertEqual(updated_event.date_hour_end.strftime('%Y-%m-%dT%H:%M:%SZ'), '2024-03-25T14:00:00Z')
        self.assertEqual(updated_event.description, 'Updated Event Description')

    def test_get_all_events(self):
        url = reverse('get_all_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_event_by_id(self):
        event = Event.objects.create(owner=self.user, date_hour_initial='2024-03-25T08:00:00Z', date_hour_end='2024-03-25T12:00:00Z', address=self.address, description='Test Event')
        url = reverse('event-detail', kwargs={'pk': event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_event(self):
        event = Event.objects.create(owner=self.user, date_hour_initial='2024-03-25T08:00:00Z', date_hour_end='2024-03-25T12:00:00Z', address=self.address, description='Test Event')
        url = reverse('search-event')
        response = self.client.get(url, {'city': 'Test City'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
