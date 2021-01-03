from django.urls import path
from . import views


app_name = 'weather'

urlpatterns = [
    path("<str:base_date>/<str:base_time>/<int:nx>/<int:ny>/", views.weatherGetInfo, name="weather"),
]