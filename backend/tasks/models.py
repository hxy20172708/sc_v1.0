from django.db import models
import uuid
from resources.models import Server

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', '待执行'),
        ('running', '执行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    command = models.TextField()
    servers = models.ManyToManyField(Server, related_name='tasks')
    schedule = models.CharField(max_length=100, help_text="Cron表达式格式: 分 时 日 月 周")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    last_execution = models.DateTimeField(null=True, blank=True)
    next_execution = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class TaskResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='results')
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    output = models.TextField(blank=True)
    error = models.TextField(blank=True)
    exit_code = models.IntegerField(null=True, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.name} on {self.server.name} at {self.executed_at}"

    class Meta:
        ordering = ['-executed_at']
