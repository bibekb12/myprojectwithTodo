from rest_framework import serializers
from .models import Todo
from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer

class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields= ["id","email","username","password"]

class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields= ["id","email","username","password"]


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id","task", "completed", "timestamp", "updated", "user"]