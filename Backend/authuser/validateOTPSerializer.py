from rest_framework import serializers


class ValidateOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField()