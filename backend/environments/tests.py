from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Environment
from resources.models import Room, Server
from accounts.models import User

class EnvironmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.room = Room.objects.create(name='Test Room')
        self.server = Server.objects.create(
            name='Test Server',
            ip_address='192.168.1.1',
            room=self.room
        )
        
        self.environment_url = reverse('environment-list')
        self.environment_data = {
            'name': 'Test Environment',
            'description': 'Test Description',
            'server_ids': [str(self.server.id)]
        }

    def test_create_environment(self):
        response = self.client.post(self.environment_url, self.environment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Environment.objects.count(), 1)
        self.assertEqual(Environment.objects.get().name, 'Test Environment')
        self.assertEqual(Environment.objects.get().servers.count(), 1)
