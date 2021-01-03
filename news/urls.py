from django.urls import path
from . import views


app_name = "news"

urlpatterns = [
    path("<str:query>/", views.crawler, name="news"),
]