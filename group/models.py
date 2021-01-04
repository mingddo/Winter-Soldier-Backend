from django.db import models
from django.conf import settings

# Create your models here.
class Group(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group')
    inviting = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='invited')
    name = models.CharField(max_length=20)
    master = models.CharField(max_length=50)
    introduce = models.TextField()


class GroupTodo(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_todo")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="group_todo")
    title = models.CharField(max_length=100)
    content = models.TextField()
    schedule_year = models.CharField(max_length=4)
    schedule_month = models.CharField(max_length=2)
    schedule_date = models.CharField(max_length=2)
    schedule_hour = models.CharField(max_length=2)
    schedule_min = models.CharField(max_length=2)

    def __str__(self):
        return self.title
