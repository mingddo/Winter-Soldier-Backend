from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Todo
from .serializers import TodoSerializer
import json
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.


@api_view(["GET", "POST"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def todo_list_create(request):
    if request.method == "GET":
        todos = Todo.objects.all().filter(user=request.user)

        context = {
            "username": request.user.username,
            "userid": request.user.id,
        }
        todolist = {}

        for t in todos:
            t_dict = {}
            t_dict["id"] = t.id
            t_dict["title"] = t.title
            t_dict["schedule_year"] = t.schedule_year
            t_dict["schedule_month"] = t.schedule_month
            t_dict["schedule_date"] = t.schedule_date
            t_dict["schedule_hour"] = t.schedule_hour
            t_dict["schedule_min"] = t.schedule_min
            t_dict["alarm_year"] = t.alarm_year
            t_dict["alarm_month"] = t.alarm_month
            t_dict["alarm_date"] = t.alarm_date
            t_dict["alarm_hour"] = t.alarm_hour
            t_dict["alarm_min"] = t.alarm_min
            t_dict["completed"] = t.completed
            t_dict["user_id"] = t.user_id

            date = str(t.alarm_year) + str(t.alarm_month) + str(t.alarm_date)
            if date in todolist:

                todolist[date].append(t_dict)

            else:
                t_l = []
                t_l.append(t_dict)
                todolist[date] = t_l

        context["todolist"] = todolist
        # print(request.user.my_todo)
        # serializer = TodoSerializer(request.user.my_todo, many=True)
        # print(serializer.data)
        # return Response(serializer.data)
        return Response(context)
    else:
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)


@api_view(["PUT", "DELETE"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def todo_update_delete(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    print(request.user.id, todo.user)
    if request.user == todo.user:
        if request.method == "PUT":
            serializer = TodoSerializer(todo, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            todo.delete()
            return Response({"삭제된 todo_id": todo_pk})
    else:
        return Response({"detail": "권한이 없습니다."})
