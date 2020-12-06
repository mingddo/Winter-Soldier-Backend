from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.todo_list_create),
    path('<int:todo_pk>/', views.todo_update_delete),
]
