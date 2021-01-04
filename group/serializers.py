from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Group, GroupTodo

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('user', 'master', 'group_todo', 'inviting', 'name', 'introduce')
        depth = 1
        read_only_fields = ('user', 'master', 'inviting', 'group_todo')


class GroupTodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupTodo
        fields = '__all__'
        read_only_fields = ('group',)
        depth = 1