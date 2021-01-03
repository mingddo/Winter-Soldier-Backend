from django.urls import path
from . import views

app_name = "stocks"

urlpatterns = [
    path("<str:companycode>/<int:period>/", views.stocks, name="stocks"),
]
