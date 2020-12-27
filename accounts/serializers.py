from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', )

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username',)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        depth = 1
        fields = ('id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'my_todo')