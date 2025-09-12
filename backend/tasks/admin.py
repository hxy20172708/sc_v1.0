from django.contrib import admin
from .models import Task, TaskResult

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'command', 'schedule', 'status', 'last_execution')
    search_fields = ('name', 'command')
    list_filter = ('status',)
    filter_horizontal = ('servers',)

@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ('task', 'server', 'exit_code', 'executed_at')
    search_fields = ('task__name', 'server__name', 'output', 'error')
    list_filter = ('exit_code', 'executed_at')
