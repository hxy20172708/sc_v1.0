from rest_framework import serializers
from .models import Task, TaskResult
from resources.serializers import ServerSerializer


class TaskSerializer(serializers.ModelSerializer):
    server_list = ServerSerializer(source='servers', many=True, read_only=True)
    # 使用ListField处理多个UUID
    server_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'status', 'last_execution', 'next_execution', 'created_at', 'updated_at')


class TaskResultSerializer(serializers.ModelSerializer):
    server_name = serializers.ReadOnlyField(source='server.name')
    task_name = serializers.ReadOnlyField(source='task.name')

    class Meta:
        model = TaskResult
        fields = '__all__'
        read_only_fields = ('id', 'executed_at')
