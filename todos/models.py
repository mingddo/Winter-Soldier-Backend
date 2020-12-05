from django.db import models
from django.conf import settings

class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    schedule_at = models.DateTimeField()
    alarm_at = models.DateTimeField()