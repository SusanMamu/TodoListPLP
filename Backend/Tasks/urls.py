from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TasksView

router = DefaultRouter()
router.register(r'', TasksView, basename='Tasks')

urlpatterns = [
    path('', include(router.urls)),
]
