from django.db import models
from django.conf import settings


class Todo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_todo"
    )
    title = models.CharField(max_length=100)
    schedule_year = models.CharField(max_length=4)
    schedule_month = models.CharField(max_length=2)
    schedule_date = models.CharField(max_length=2)
    schedule_hour = models.CharField(max_length=2)
    schedule_min = models.CharField(max_length=2)
    alarm_year = models.CharField(max_length=4)
    alarm_month = models.CharField(max_length=2)
    alarm_date = models.CharField(max_length=2)
    alarm_hour = models.CharField(max_length=2)
    alarm_min = models.CharField(max_length=2)
    completed = models.CharField(max_length=10, default="no")

    def __str__(self):
        return self.title
