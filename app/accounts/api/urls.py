"""
Accounts Api urls
"""
from django.urls import path
from accounts.api.views import (
    LogoutAPIView, RegisterAPIView, UserListView, UserAPIView, CurrentUserAPIView, CustomAuthToken
)

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='api_register'),
    path('login', CustomAuthToken.as_view(), name="api_login"),
    path('logout/', LogoutAPIView.as_view(), name="api_logout"),
    path('users', UserListView.as_view(), name='api_show_users'),
    path('current_user/', CurrentUserAPIView.as_view(), name='api_current_user'),
    path('users/<employee_type>', UserListView.as_view(), name='api_users_type'),
    path('users/<int:pk>', UserAPIView.as_view(), name="api_rud_user"),
]
