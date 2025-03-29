from django.shortcuts import render
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# TODO: Add authentication

# TODO: Add create_user, delete_user, update_user

from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet): 
    """
    Only admin user is able to view all users.
    Regular user can view only their own info.

    ## Examples:
    ### GET /api/users/
    -  Returns full user list (only for admin)

    ### GET /api/users/me/
    -  Returns info about the current logged-in user (for anyone logged in)

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["get"], url_path="me", permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Return the authenticated user's own info.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
