from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FavoriteEvent
from user.models import CustomUser
from event.models import Event
from address.models import Address

class FavoriteEventTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword', type=2)
        self.address = Address.objects.create(city='Test City', street='Test Street', number='123')
        self.event = event = Event.objects.create(owner=self.user, date_hour_initial='2024-03-25T08:00:00Z', date_hour_end='2024-03-25T12:00:00Z', address=self.address, description='Test Event')
        self.client.force_authenticate(user=self.user)

    def test_add_favorite_event(self):
        url = reverse('add_favorite_event', kwargs={'event_id': self.event.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FavoriteEvent.objects.filter(user=self.user, event=self.event).exists())

    def test_remove_favorite_event(self):
        FavoriteEvent.objects.create(user=self.user, event=self.event)
        url = reverse('remove_favorite_event', kwargs={'event_id': self.event.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(FavoriteEvent.objects.filter(user=self.user, event=self.event).exists())

    def test_list_favorite_events(self):
        FavoriteEvent.objects.create(user=self.user, event=self.event)
        url = reverse('list_favorite_events_by_user_id')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['description'], 'Test Event')
