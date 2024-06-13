
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GetMethod

router = DefaultRouter()
router.register(r'', GetMethod, basename='')


urlpatterns = [
    path('findByEmail/<str:email>/', GetMethod.as_view({'get': 'fetchByEmail'}), name='fetchByEmail'),
    path('', include(router.urls)),
]
