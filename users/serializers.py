from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import CustomUser

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Email должен быть на @gmail.com")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Пароль должен быть не менее 6 символов")
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

    def authenticate_user(self):
        user = authenticate(
            email=self.validated_data['email'],
            password=self.validated_data['password']
        )
        if user is None:
            raise serializers.ValidationError("Неверный email или пароль")
        return user
