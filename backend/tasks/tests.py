from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
from resources.models import Room, Server
from accounts.models import User

class TaskTests(TestCase):
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
        
        self.task_url = reverse('task-list')
        self.task_data = {
            'name': 'Test Task',
            'command': 'ls -la',
            'schedule': '0 * * * *',
            'server_ids': [str(self.server.id)]
        }

    def test_create_task(self):
        response = self.client.post(self.task_url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, 'Test Task')
        self.assertEqual(Task.objects.get().servers.count(), 1)
