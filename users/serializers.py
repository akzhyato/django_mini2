from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser
from djoser.serializers import UserCreateSerializer


class UserSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'},
                                     )
    username = serializers.CharField()
    role = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'password']


class CustomUserSerializer(UserSerializer):
    email = serializers.EmailField(help_text="The user's email address.")
    username = serializers.CharField(help_text="The user's username.")
    role = serializers.CharField(help_text="The role of the user (e.g., 'student', 'teacher', 'admin').")

    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'role')
