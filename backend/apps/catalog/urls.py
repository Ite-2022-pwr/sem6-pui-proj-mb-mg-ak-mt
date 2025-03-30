from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *




router = DefaultRouter()
# this will be under /api/genres/
router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet, basename='movie')

## Every url here will ne prepended with /api/
urlpatterns = [
    path('', include(router.urls)),
]
