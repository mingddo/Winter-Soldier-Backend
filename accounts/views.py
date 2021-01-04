from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserinfoSerializer, UserListSerializer, ProfileSerializer, UserFollowerSerailizer
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