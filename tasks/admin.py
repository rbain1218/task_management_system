from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_assigned_users', 'created_by', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description', 'assigned_to__username')

    def get_assigned_users(self, obj):
        return ", ".join([user.username for user in obj.assigned_to.all()])
    
    get_assigned_users.short_description = "Assigned To"
