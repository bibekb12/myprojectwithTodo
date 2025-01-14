from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated


class TodoListApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List all the todo items for the given requested user
        """
        todos = Todo.objects.filter(user=request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """create the Todo with the given data"""
        data = {
            "task": request.data.get("task"),
            "completed": request.data.get("completed"),
            "user": request.user.id,
        }
        serialzer = TodoSerializer(data=data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        """helper mehtod to get the object with todo_id and user_id"""
        try:
            return Todo.objects.get(id=todo_id, user=user_id)
        except Todo.DoesNotExist:
            return None

    def get(self, request, todo_id, *args, **kwargs):
        """Retrive the todo with given todo_id"""
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"error": "object with id donot exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, todo_id, *args, **kwargs):
        """Updates the todo item with given todo_id if exists"""
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"error": "objects with the given data does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "task": request.data.get("task"),
            "completed": request.data.get("completed", todo_instance.completed),
            "user": request.user.id,
        }
        serializer = TodoSerializer(instance=todo_instance,data= data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,todo_id, *args, **kwargs):
        '''Deletes the todo item with the given id'''
        todo_instance = self.get_object(todo_id,request.user.id)
        if not todo_instance:
            return Response(
                {"error":"object with given id not matched"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"ok":"Todo item deleted."}, status=status.HTTP_410_GONE
        )