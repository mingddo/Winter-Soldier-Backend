from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Group, GroupTodo
from .serializers import GroupSerializer, GroupTodoSerializer

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# Create your views here.
# 그룹 기능 추가
# 1. 그룹 만들기 -> 만든 사람은 그룹원인 동시에 그룹장이 될 수 있다. GET -> 그룹 조회 / POST -> 그룹 생성
# 1-1. 그룹 디테일 조회 -> 그룹원들은 그룹을 조회할 수 있다. GET -> 그룹조회 / DELETE -> 그룹삭제(그룹장만 권한을 가질 수 있다.)
# 2. 그룹 초대하기 -> 그룹원들은 그룹원이 아닌 사람들 그룹에 초대할 수 있다. -> POST 초대 / DELETE 초대 취소 ( 혹은 초대 거절/ 초대 리스트에서 삭제)
# 3. 그룹 멤버 추가 -> 초대받은 유저는 초대를 응하여 그룹의 멤버가 될 수 있다. 그룹장과 본인은 그룹에서 강퇴시키거나 나갈 수 있다.-> POST 초대 ok / DELETE 멤버 삭제
# 4. 그룹장 위임 -> 그룹장 본인은 선택한 유저에게 master 직위를 넘겨줄 수 있다. 
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group(request):
    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_group = serializer.save()
            new_group.user.add(request.user)
            new_group.master = request.user.username
            new_group.save()
            return Response({'group': new_group.name})
    else:
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_detail(request, group_pk):
    thisgroup = get_object_or_404(Group, pk=group_pk)
    if request.method == 'GET':
        if request.user in thisgroup.user.all():
            serializer = GroupSerializer(thisgroup)
            return Response(serializer.data)
        else:
            return Response({'error': '그룹원들만 확인 가능합니다.'})
    else:
        if request.user.username == thisgroup.master:
            thisgroup.delete()
            return Response({'deleted_group': thisgroup.name})
    return Response({'error': '권한이 없습니다.'}) 


@api_view(['GET', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_invite(request, group_pk, username):
    thisgroup = get_object_or_404(Group, pk=group_pk)
    person = get_object_or_404(get_user_model(), username=username)
    if person in thisgroup.user.all():
        return Response({'error': f'{person.username}님은 이미 그룹에 소속되어있습니다.'})
    if request.method == 'GET':
        if request.user in thisgroup.user.all():
            thisgroup.host = request.user.username
            thisgroup.save()
            thisgroup.inviting.add(person)
            return Response({'invite': person.username})
        else:
            return Response({'error': '그룹원들만 초대 가능합니다'})
    else:
        if person in thisgroup.inviting.all():
            thisgroup.inviting.remove(person)
            return Response({'cancel': person.username})
        else:
            return Response({'error': f'{person.username}님은 초대 받지 않으셨습니다'})



@api_view(['GET', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_member(request, group_pk, username):
    thisgroup = get_object_or_404(Group, pk=group_pk)
    person = get_object_or_404(get_user_model(), username=username)
    if request.method == 'GET':
        if person in thisgroup.inviting.all() and request.user == person:
            thisgroup.inviting.remove(person)
            thisgroup.user.add(person)
            return Response({'newmember': person.username})
        
    else:
        if request.user.username == thisgroup.master or request.user == person:
            thisgroup.user.remove(person)
            return Response({'leaveuser': person.username})
    return Response({'error': '권한이 없습니다.'}) 


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_master(request, group_pk, username):
    thisgroup = get_object_or_404(Group, pk=group_pk)
    person = get_object_or_404(get_user_model(), username=username)
    if request.user.username == thisgroup.master:
        thisgroup.master = person.username
        thisgroup.save()
        return Response({'newmaster': person.username})
    else:
        return Response({'error': '권한이 없습니다.'}) 


@api_view(["GET", "POST"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_todo_list(request, group_pk):
    thisgroup = get_object_or_404(Group, pk=group_pk)
    if request.user not in thisgroup.user.all():
        return Response({'error': '권한이 없습니다.'}) 
    if request.method == 'GET':
        todos = GroupTodo.objects.all().filter(group=group_pk)
        context = {}
        todolist = {}
        for t in todos:
            t_dict = {}
            t_dict["id"] = t.id
            t_dict["title"] = t.title
            t_dict["content"] = t.content
            t_dict["schedule_year"] = t.schedule_year
            t_dict["schedule_month"] = t.schedule_month
            t_dict["schedule_date"] = t.schedule_date
            t_dict["schedule_hour"] = t.schedule_hour
            t_dict["schedule_min"] = t.schedule_min
            t_dict["group_id"] = t.group_id
            t_dict["user_id"] = t.user_id
            if len(str(t.schedule_month)) < 2:
                t.schedule_month = "0" + str(str(t.schedule_month))
            if len(str(t.schedule_date)) < 2:
                t.schedule_date = "0" + str(str(t.schedule_date))
            date = str(t.schedule_year) + t.schedule_month + t.schedule_date
            if date in todolist:

                todolist[date].append(t_dict)

            else:
                t_l = []
                t_l.append(t_dict)
                todolist[date] = t_l

        context["todolist"] = todolist

        return Response(context)
    else:
        serializer = GroupTodoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, group=thisgroup)
        return Response(serializer.data)


@api_view(["PUT", "DELETE"])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_todo_update_delete(request, group_pk, todo_pk):
    thisgroup = get_object_or_404(Group, pk=group_pk)
    todo = thisgroup.group_todo.all().filter(pk=todo_pk).first()
    if request.user not in thisgroup.user.all():
        return Response({'error': '권한이 없습니다.'}) 
    if request.method == "PUT":
        serializer = GroupTodoSerializer(todo, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        todo.delete()
        return Response({"삭제된 todo_id": todo_pk})
