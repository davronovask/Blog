from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'nickname',
            'password',
            'password2'
        ]

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Email должен быть на @gmail.com")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Email должен быть на @gmail.com")
        return value

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Неверный email или пароль")
        data['user'] = user
        return data
