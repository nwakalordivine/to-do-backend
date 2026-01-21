from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'created_at', 'status']