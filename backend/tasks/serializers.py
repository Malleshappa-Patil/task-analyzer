from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # Explicitly define dependencies to handle list of IDs
    dependencies = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Task.objects.all(), 
        required=False
    )
    
    # Read-only field for the calculated score
    priority_score = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = [
            'id', 
            'title', 
            'due_date', 
            'estimated_hours', 
            'importance', 
            'dependencies', 
            'priority_score',
            'completed'
        ]

    def validate_importance(self, value):
        """Ensure importance is strictly 1-10 as per requirements [cite: 30]"""
        if not (1 <= value <= 10):
            raise serializers.ValidationError("Importance must be between 1 and 10.")
        return value