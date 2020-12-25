from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('<str:companyname>/', views.stocks, name="stocks"),
]
