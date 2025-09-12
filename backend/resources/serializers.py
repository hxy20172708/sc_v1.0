from rest_framework import serializers
from .models import Room, Server

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class ServerSerializer(serializers.ModelSerializer):
    room_name = serializers.ReadOnlyField(source='room.name')
    
    class Meta:
        model = Server
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'last_check')
