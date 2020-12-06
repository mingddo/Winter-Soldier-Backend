from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer
# Create your views here.

@api_view(['GET','POST'])
def todo_list_create(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    else:
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def todo_update_delete(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    if request.user == todo.user:
        if request.method == 'PUT':
            serializer = TodoSerializer(todo, request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            todo.delete()
            return Response(status=status.HTTP_200)

        
