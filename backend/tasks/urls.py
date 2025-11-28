from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, AnalyzeTasksView, SuggestTasksView

router = DefaultRouter()
router.register(r'all', TaskViewSet) # Access at /api/tasks/all/

urlpatterns = [
    # Router URLs (CRUD)
    path('', include(router.urls)),
    
    # Custom Endpoints
    path('analyze/', AnalyzeTasksView.as_view(), name='analyze-tasks'),
    path('suggest/', SuggestTasksView.as_view(), name='suggest-tasks'),
]