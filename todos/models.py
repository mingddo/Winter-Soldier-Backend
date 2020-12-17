from django.db import models
from django.conf import settings

class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_todo")
    title = models.CharField(max_length=100)
    schedule_year = models.IntegerField
    schedule_month = models.IntegerField()
    schedule_date = models.IntegerField()
    schedule_hour = models.IntegerField()
    schedule_min = models.IntegerField()
    alarm_year = models.IntegerField()
    alarm_month = models.IntegerField()
    alarm_date = models.IntegerField()
    alarm_hour = models.IntegerField()
    alarm_min = models.IntegerField()

    def __str__(self):
        return self.title
    