from django.urls import path

from .views import ServicesView

urlpatterns = [
    path('services/', ServicesView.as_view({'get': 'read_services'}), name='read_services'),

]


