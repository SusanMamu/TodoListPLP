from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import CustomUser


class ResetPassSerializer(serializers.Serializer):
    # class Meta:
    #     model = CustomUser
    #     fields = ' email = serializers.EmailField(),password = serializers.CharField()'

    email = serializers.EmailField()
    phone_number = serializers.IntegerField()
    # resetpassword = serializers.CharField()

    def create(self, validated_data):
        # Hash the password before saving it
        validated_data['resetpassword'] = make_password(validated_data.get('resetpassword'))
        return super( ResetPassSerializer, self).create(validated_data)
