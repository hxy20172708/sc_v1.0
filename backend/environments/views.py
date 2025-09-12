from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Environment
from .serializers import EnvironmentSerializer
from resources.models import Server

class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    def perform_create(self, serializer):
        environment = serializer.save()
        # 处理服务器ID
        if 'server_ids' in self.request.data:
            server_ids = self.request.data.getlist('server_ids')
            servers = Server.objects.filter(id__in=server_ids)
            environment.servers.set(servers)
    
    def perform_update(self, serializer):
        environment = serializer.save()
        # 处理服务器ID
        if 'server_ids' in self.request.data:
            server_ids = self.request.data.getlist('server_ids')
            servers = Server.objects.filter(id__in=server_ids)
            environment.servers.set(servers)
