from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', )

class UserList(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username',)