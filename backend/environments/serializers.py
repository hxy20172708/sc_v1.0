from rest_framework import serializers
from .models import Environment
from resources.serializers import ServerSerializer


class EnvironmentSerializer(serializers.ModelSerializer):
    servers_detail = serializers.SerializerMethodField()
    # 修复：使用ListField处理多个UUID
    server_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Environment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_servers_detail(self, obj):
        servers = obj.servers.all()
        return [{
            'id': server.id,
            'name': server.name,
            'ip_address': server.ip_address,
            'room': server.room.name if server.room else None,
            'status': server.status
        } for server in servers]
