from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Room, Server
from .serializers import RoomSerializer, ServerSerializer
import socket
from datetime import datetime

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location']
    ordering_fields = ['name', 'created_at']

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['room', 'status', 'os']
    search_fields = ['name', 'ip_address', 'hostname', 'os', 'cpu']
    ordering_fields = ['name', 'ip_address', 'status', 'created_at']
    
    @action(detail=True, methods=['get'])
    def check_status(self, request, pk=None):
        server = self.get_object()
        try:
            # 尝试连接服务器的22端口（SSH）
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                result = s.connect_ex((server.ip_address, 22))
                if result == 0:
                    server.status = 'online'
                else:
                    server.status = 'offline'
            server.last_check = datetime.now()
            server.save()
            return Response({'status': server.status})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def get_config(self, request, pk=None):
        server = self.get_object()
        # 这里简化处理，实际应用中应该通过SSH连接获取真实配置
        try:
            # 模拟获取配置信息
            # 实际应用中应该使用paramiko等库通过SSH连接服务器
            server.os = "Ubuntu 20.04 LTS"
            server.cpu = "Intel Xeon E5-2670 v3"
            server.memory = "32GB"
            server.disk = "500GB SSD"
            server.network_speed = "1Gbps"
            server.save()
            
            serializer = self.get_serializer(server)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
