from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer
from .scoring import calculate_task_score

# Standard CRUD ViewSet (List, Create, Delete, Update)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        # Calculate score immediately upon saving
        instance = serializer.save()
        instance.priority_score = calculate_task_score(instance, is_dict=False)
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.priority_score = calculate_task_score(instance, is_dict=False)
        instance.save()

# Specialized Endpoint: /api/tasks/analyze/ (POST)
class AnalyzeTasksView(APIView):
    """
    Accepts a list of tasks (JSON), calculates scores dynamically, 
    and returns them sorted. Does NOT save to DB (Stateless).
    """
    def post(self, request):
        tasks_data = request.data
        if not isinstance(tasks_data, list):
            return Response(
                {"error": "Expected a list of tasks"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        analyzed_tasks = []
        for task in tasks_data:
            # Calculate score
            score = calculate_task_score(task, is_dict=True)
            task['priority_score'] = score
            analyzed_tasks.append(task)

        # Sort: Highest score first
        sorted_tasks = sorted(
            analyzed_tasks, 
            key=lambda x: x['priority_score'], 
            reverse=True
        )

        return Response(sorted_tasks)

# Specialized Endpoint: /api/tasks/suggest/ (GET)
class SuggestTasksView(APIView):
    """
    Returns the top 3 tasks from the Database that the user should do today.
    """
    def get(self, request):
        # 1. Get incomplete tasks
        tasks = Task.objects.filter(completed=False)
        
        # 2. Re-calculate scores (to ensure date math is fresh)
        task_list = []
        for task in tasks:
            task.priority_score = calculate_task_score(task, is_dict=False)
            task.save() # Update DB with fresh score
            task_list.append(task)
            
        # 3. Sort
        task_list.sort(key=lambda x: x.priority_score, reverse=True)
        
        # 4. Pick Top 3
        top_tasks = task_list[:3]
        serializer = TaskSerializer(top_tasks, many=True)
        
        # 5. Add "Why?" explanation
        response_data = []
        for data in serializer.data:
            explanation = "High Priority."
            if data['priority_score'] > 80:
                explanation = "Urgent deadline approaching!"
            elif data['importance'] >= 8:
                explanation = "Marked as very important."
            elif data['estimated_hours'] <= 2:
                explanation = "Quick win - easy to complete."
            
            data['suggestion_reason'] = explanation
            response_data.append(data)

        return Response(response_data)