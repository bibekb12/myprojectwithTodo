from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer

class TodoListApiView(APIView):
    permission_classes= [permissions.IsAuthenticated]

    def get(self,request, *args, **kwargs):
        """
        List all the todo items for the given requested user
        """
        todos = Todo.objects.filter(user= request.user.id)
        serializer = TodoSerializer(todos, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request,*args, **kwargs):
        """create the Todo with the given data
        """
        data={
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serialzer= TodoSerializer(data=data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data,status=status.HTTP_201_CREATED)
        return Response(serialzer.errors,status=status.HTTP_400_BAD_REQUEST)
    
