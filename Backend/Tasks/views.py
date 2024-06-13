from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Tasks.models import Task
from Tasks.serializers import TaskSerializer
from utils.ApiResponse import ApiResponse


class TasksView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    #authentication_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = ApiResponse()
        tasks = Task.objects.all()
        serializer = self.get_serializer(tasks, many=True)
        response.setStatusCode(status.HTTP_200_OK)
        response.setMessage("Found")
        response.setEntity(serializer.data)
        return Response(response.toDict(), status=response.status)

    def create(self, request, *args, **kwargs):
        response = ApiResponse()
        tasks_data = TaskSerializer(data=request.data)
        if tasks_data.is_valid():
            check_id = request.data.get("taskId")
            existing_task = Task.objects.filter(id=check_id).first()
            if existing_task:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({"message": "Task already exists.", "status": status_code}, status=status_code)
            tasks_data.save()
            response.setStatusCode(status.HTTP_201_CREATED)
            response.setMessage("Task added")
            response.setEntity(request.data)
            return Response(response.toDict(), status=response.status)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Please fill in the details correctly.", "status": status_code},
                            status=status_code)

    def destroy(self, request, *args, **kwargs):
        response = ApiResponse()
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"message": "Task deleted successfully", "status": status.HTTP_200_OK})
        except Task.DoesNotExist:
            return Response({"message": "Task data not found", "status": status.HTTP_400_BAD_REQUEST})

    def update(self, request, *args, **kwargs):
        response = ApiResponse()
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Task updated successfully", "status": status.HTTP_200_OK})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({"message": "Task data not found", "status": status.HTTP_400_BAD_REQUEST})