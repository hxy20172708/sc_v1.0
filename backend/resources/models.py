from django.db import models
import uuid

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机房"
        verbose_name_plural = "机房"
        ordering = ['name']

class Server(models.Model):
    STATUS_CHOICES = (
        ('online', '在线'),
        ('offline', '离线'),
        ('maintenance', '维护中'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(unique=True)
    hostname = models.CharField(max_length=200, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='servers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    os = models.CharField(max_length=100, blank=True, verbose_name="操作系统")
    cpu = models.CharField(max_length=100, blank=True)
    memory = models.CharField(max_length=50, blank=True)
    disk = models.CharField(max_length=100, blank=True)
    network_speed = models.CharField(max_length=50, blank=True)
    last_check = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'room']
