from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ServerViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'servers', ServerViewSet, basename='server')

urlpatterns = [
    path('', include(router.urls)),
]
