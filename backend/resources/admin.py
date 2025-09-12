from django.contrib import admin
from .models import Room, Server

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at',)

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'room', 'status', 'os')
    search_fields = ('name', 'ip_address', 'hostname', 'os')
    list_filter = ('status', 'os', 'room')
