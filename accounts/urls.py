from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('signup/', views.signup),
    path('api_token_auth/', obtain_jwt_token),
    path('delete/<username>/', views.userdelete),
    path('userlist/', views.get_userlist),
    path('userlist/<keyword>/', views.find_userlist),
    path('profile/<username>/', views.get_profile),
    path('follow/<username>/', views.follow),
]
