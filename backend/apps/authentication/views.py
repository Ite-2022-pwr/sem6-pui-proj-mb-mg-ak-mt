from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *



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
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username,
        })

###### LOGOUT ######
class LogoutView(APIView):
    """
    Logout the user and delete the token

    ## POST
    
    Requires authetication token

    ### Returns:
    401 -- If user did not provide auth token or is invalid\n
    200 -- if logged out user successfully

    ### Example:
    curl -X POST http://localhost:8000/api/auth/logout/ \
    -H "Authorization: Token <token>"

    """
    permission_classes = [IsAuthenticated]

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
    200 - with id, username, email \n
    400 - If user already exists
    400 - If the password does not meet the requirements
    400 - If the email address is invalid

    ### Example:
    curl -w "%{http_code}\n" -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser2", "email": "user@example.com", "password": "asdfasdfasdf123"}'


    """



    permission_classes = [AllowAny]  # It allows everybody to access this endpoint
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
