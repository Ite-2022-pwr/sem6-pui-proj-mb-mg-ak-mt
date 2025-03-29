from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token  # fallback if you don't customize

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    #TODO:  add logout, register, change-password etc. dunno yet if here
    # or in users module
]
