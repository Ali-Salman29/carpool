"""
Api View File
"""
from rest_framework import generics, views
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from accounts.models import CustomUser
from accounts.api.serializers import RegisterSerializer, UserSerializer
from accounts.api.permissions import IsUser


class RegisterAPIView(generics.CreateAPIView):
    """
    User Registration Api View
    """
    serializer_class = RegisterSerializer


class CurrentUserAPIView(generics.RetrieveAPIView):
    """
    User Registration Api View
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get Authenticated User
        """
        user = UserSerializer(request.user)
        content = {
            'user': user.data,
            'auth': str(request.auth)
        }
        return Response(content)


class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    User Update View
    """
    permission_classes = [IsAuthenticated, IsUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    """
    Show All users
    """
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class LogoutAPIView(views.APIView):
    """
    Logout User
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        Logout User
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
