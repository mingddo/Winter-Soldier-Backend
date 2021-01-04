from django.urls import path
from . import views


app_name = "news"

urlpatterns = [
    path("crawler/<str:query>/", views.crawler, name="news"),
    path("daymost/", views.daymost, name="daymost"),
]