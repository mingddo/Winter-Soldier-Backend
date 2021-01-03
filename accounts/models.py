from django.db import models
from django.contrib.auth.models import AbstractUser
import sys ; sys.path.append('/dir/of/todos')
from todos.models import Todo

class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings')


class Group(models.Model):
    user = models.ManyToManyField(User, related_name='group')
    inviting = models.ManyToManyField(User, related_name='invited')
    name = models.CharField(max_length=20)
    master = models.CharField(max_length=50)
    todo = models.ManyToManyField(Todo, related_name="group_Todo")
