from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserinfoSerializer, UserListSerializer, ProfileSerializer, UserFollowerSerailizer, GroupSerializer
from .models import User, Group
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# Create your views here.
@api_view(['POST'])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def userdelete(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    if request.user == person:
        person.delete()
        return Response({'deleted_user': person.username})
    else:
        return Response({'error': '권한이 없습니다.'}) 


@api_view(['GET'])
def get_userlist(request):
    user = get_user_model()
    users = user.objects.all()
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
     

@api_view(['GET'])
def find_userlist(request, keyword):
    user = get_user_model()
    users = user.objects.all()
    value = user.objects.filter(username__startswith=keyword)
    seriailizer = UserListSerializer(value, many=True)
    return Response(seriailizer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    serializer = ProfileSerializer(user)
    return Response(serializer.data)
    

@api_view(['POST', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def follow(request, username):
    me = request.user
    person = get_object_or_404(get_user_model(), username=username)
    if me != person:
        if request.method == 'POST':
            follow = person.followers.add(me)
            serializer = UserFollowerSerailizer(follow, many=True)
            return Response({'username' : person.username}, status=status.HTTP_200_OK)
        else:
            follow_cancel = person.followers.remove(me)
            serializer = UserFollowerSerailizer(follow_cancel, many=True)
            return Response({'username' : person.username}, status=status.HTTP_200_OK)
    else:
        return Response({'error':'본인은 팔로우할 수 없습니다.'})


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


@api_view(['POST', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_invite(request, group_pk, username):
    thisgroup = get_object_or_404(Group, pk=group_pk)
    person = get_object_or_404(get_user_model(), username=username)
    if request.user in thisgroup.user.all() and person not in thisgroup.user.all():
        if request.method == 'POST':
            thisgroup.inviting.add(person)
            return Response({'invite': person.username})
        else:
            thisgroup.inviting.remove(person)
            return Response({'cancel': person.username})
    return Response({'error': '그룹원들만 초대 가능합니다'})


@api_view(['POST', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_member(request, group_pk, username):
    thisgroup = get_object_or_404(Group, pk=group_pk)
    person = get_object_or_404(get_user_model(), username=username)
    if request.method == 'POST':
        if person in thisgroup.inviting.all() and request.user == person:
            thisgroup.inviting.remove(person)
            thisgroup.user.add(person)
            return Response({'newmember': person.username})
        
    else:
        if request.user.username == thisgroup.master or request.user == person:
            thisgroup.user.remove(person)
            return Response({'leaveuser': person.username})
    return Response({'error': '권한이 없습니다.'}) 


@api_view(['POST'])
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