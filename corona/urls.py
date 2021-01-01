from django.urls import path
from . import views


urlpatterns = [
    path("", views.getInfo),
    path("city/", views.getcityInfo),
]
