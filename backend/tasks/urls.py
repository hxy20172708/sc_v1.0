from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskResultViewSet

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')
router.register(r'results', TaskResultViewSet, basename='task-result')

urlpatterns = [
    path('', include(router.urls)),
]
