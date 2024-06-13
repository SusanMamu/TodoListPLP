from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
# from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.ApiResponse import ApiResponse

from .serializers import *


class GetMethod(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        response = ApiResponse()
        data = list(CustomUser.objects.all().values())
        response.setStatusCode(status.HTTP_200_OK)
        response.setMessage("Found")
        response.setEntity(data)
        return Response(response.toDict(), status=response.status)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()

        user_permissions = user.user_permissions.all()
        roles = [permission.name for permission in user_permissions]
        serializer = CustomUserSerializer(user)

        data = serializer.data
        data['roles'] = roles

        return Response(data)

    def create(self, request, *args, **kwargs):
        response = ApiResponse()
        customerData = CustomUserSerializer(data=request.data)

        if not customerData.is_valid():
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Please fill in the details correctly.", "status": status_code}, status_code)

        # Check if the email is already in use
        email = request.data.get("email")
        fname = request.data.get("first_name")
        existing_customer = CustomUser.objects.filter(email=email).first()

        if existing_customer:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Email is already in use.", "status": status_code}, status_code)

        # If email is not in use, save the new customer
        customerData.save()
        response.setStatusCode(status.HTTP_201_CREATED)
        response.setMessage("Created")
        response.setEntity(request.data)
        return Response(response.toDict(), status=response.status)

    def destroy(self, request, *args, **kwargs):
        userData = CustomUser.objects.filter(id=kwargs['pk'])
        if userData:
            userData.delete()
            status_code = status.HTTP_200_OK
            return Response({"message": "Customer deleted Successfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Customer data not found", "status": status_code})

    def update(self, request, *args, **kwargs):
        product_details = CustomUser.objects.get(id=kwargs['pk'])
        product_serializer_data = CustomUserSerializer(
            product_details, data=request.data, partial=True)
        if product_serializer_data.is_valid():
            product_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Customer Update Successfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Customer data Not found", "status": status_code})

    # @action(detail=False, methods=['GET'])
    def fetchByEmail(self, request, email):  # Extract email from query parameters
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                user_serializer = CustomUserSerializer(user)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                status_code = status.HTTP_404_NOT_FOUND
                return Response({"message": "Customer data not found", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Email parameter is required", "status": status_code})
