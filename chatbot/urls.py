from django.urls import path
from . import views

urlpatterns = [
    path('train/', views.chattrain),
    path('answer/<question>/', views.chatanswer),
]
