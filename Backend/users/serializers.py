from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password','username','first_name','last_name','email','is_verified']

    def create(self, validated_data):
        # Hash the password before saving it
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(CustomUserSerializer, self).create(validated_data)
