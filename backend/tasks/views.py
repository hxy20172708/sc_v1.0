from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, TaskResult
from .serializers import TaskSerializer, TaskResultSerializer
from resources.models import Server
import paramiko
import time
from crontab import CronTab
from datetime import datetime

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'command']
    ordering_fields = ['name', 'created_at', 'status']
    
    def perform_create(self, serializer):
        task = serializer.save()
        # 处理服务器ID
        if 'server_ids' in self.request.data:
            server_ids = self.request.data.getlist('server_ids')
            servers = Server.objects.filter(id__in=server_ids)
            task.servers.set(servers)
        
        # 解析cron表达式，设置下次执行时间
        try:
            cron = CronTab(task.schedule)
            next_run = cron.next(datetime.now())
            task.next_execution = datetime.fromtimestamp(time.time() + next_run)
            task.save()
        except Exception as e:
            print(f"Error parsing cron schedule: {e}")
    
    @action(detail=True, methods=['post'])
    def execute_now(self, request, pk=None):
        task = self.get_object()
        task.status = 'running'
        task.save()
        
        results = []
        for server in task.servers.all():
            result = TaskResult(task=task, server=server)
            try:
                # 执行命令（简化版，实际应用需处理认证）
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                # 注意：在生产环境中，应使用更安全的认证方式
                ssh.connect(server.ip_address, username='root', password='password')
                
                stdin, stdout, stderr = ssh.exec_command(task.command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                
                # 获取退出码
                exit_status = stdout.channel.recv_exit_status()
                
                result.output = output
                result.error = error
                result.exit_code = exit_status
                result.save()
                results.append(result)
                
                ssh.close()
            except Exception as e:
                result.error = str(e)
                result.exit_code = -1
                result.save()
                results.append(result)
        
        task.status = 'completed'
        task.last_execution = datetime.now()
        
        # 更新下次执行时间
        try:
            cron = CronTab(task.schedule)
            next_run = cron.next(datetime.now())
            task.next_execution = datetime.fromtimestamp(time.time() + next_run)
        except Exception as e:
            print(f"Error updating next execution: {e}")
            
        task.save()
        
        serializer = TaskResultSerializer(results, many=True)
        return Response(serializer.data)

class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['task', 'server', 'exit_code']
    ordering_fields = ['executed_at']
