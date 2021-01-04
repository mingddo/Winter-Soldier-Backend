from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('', views.group),
    path('<int:group_pk>/', views.group_detail),
    path('<int:group_pk>/invite/<username>/', views.group_invite),
    path('<int:group_pk>/member/<username>/', views.group_member),
    path('<int:group_pk>/master/<username>/', views.group_master),
    path('<int:group_pk>/todo/', views.group_todo_list),
    path('<int:group_pk>/todo/<int:todo_pk>/', views.group_todo_update_delete),
]
