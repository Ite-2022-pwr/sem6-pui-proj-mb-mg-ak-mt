from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class CustomAuthToken(ObtainAuthToken):
    """
    Login user, create a token and returns a token.

    ## POST
    Required body:

    ```
    {
    "username": "username",
    "password": "password"
    }
    ```

    ### Returns:
    200 - with token, user_id, username \n
    400 - invalid creds 

    ### Example:
    curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "username123"}'

    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_200_OK)

###### LOGOUT ######


class LogoutView(APIView):
    """
    Logout the user and delete the token

    ## POST

    Requires authetication token in the headers

    ### Returns:
    401 -- If user did not provide auth token or is invalid\n
    200 -- if logged out user successfully

    ### Example:
    curl -X POST http://localhost:8000/api/auth/logout/ \
    -H "Authorization: Token <token>"

    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description="Token required in the format 'Token <token>'",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logged out successfully."})


class RegisterView(APIView):
    """
    Register user, without logging (creating a token)

    ## POST:

    Required body:
    ```
    {
        "username": "newuser",
        "email": "user@example.com",
        "password": "newpass123"
    }
    ```

    ### Returns:
    201 - with id, username, email \n
    400 - If user already exists
    400 - If the password does not meet the requirements
    400 - If the email address is invalid

    ### Example:
    ```
    curl -w "%{http_code}" -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser2", "email": "user@example.com", "password": "asdfasdfasdf123"}'
    ```

    """

    # It allows everybody to access this endpoint
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
