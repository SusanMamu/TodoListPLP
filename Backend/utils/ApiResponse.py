from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ApiResponse(JsonResponse):
    def __init__(self, message='', status=200, entity=None, **kwargs):
        self.message = message
        self.status = status
        self.entity = entity if entity is not None else []
        self.pagination = None  # Initialize pagination data
        self.kwargs = kwargs

    def setMessage(self, message=''):
        self.message = message

    def setEntity(self, entity=[]):
        self.entity = entity

    def setStatusCode(self, status=''):
        self.status = status

    def set_pagination(self, paginator):
        # Set pagination data based on the provided Django REST framework paginator
        if isinstance(paginator, PageNumberPagination):
            self.pagination = {
                'count': paginator.page.paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': self.entity,
            }

    def toDict(self):
        data = {
            'message': self.message,
            'status': self.status,
            'entity': self.entity,
        }
        if self.pagination is not None:
            data['pagination'] = self.pagination
        data.update(self.kwargs)  # Add any additional data you want in the response
        return data

    def __str__(self):
        return str(self.toDict())
