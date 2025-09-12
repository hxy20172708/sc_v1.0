from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Room, Server
from accounts.models import User

class RoomTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client.force_authenticate(user=self.user)
        self.room_url = reverse('room-list')
        self.room_data = {
            'name': 'Test Room',
            'location': 'Test Location',
            'description': 'Test Description'
        }

    def test_create_room(self):
        response = self.client.post(self.room_url, self.room_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(Room.objects.get().name, 'Test Room')

class ServerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client.force_authenticate(user=self.user)
        self.room = Room.objects.create(name='Test Room')
        self.server_url = reverse('server-list')
        self.server_data = {
            'name': 'Test Server',
            'ip_address': '192.168.1.1',
            'room': str(self.room.id),
            'status': 'online'
        }

    def test_create_server(self):
        response = self.client.post(self.server_url, self.server_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Server.objects.count(), 1)
        self.assertEqual(Server.objects.get().name, 'Test Server')
