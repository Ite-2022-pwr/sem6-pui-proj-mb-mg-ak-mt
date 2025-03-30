from django.contrib import admin
from .models import *



# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'release_date', 'vote_average', 'adult')
    list_filter = ('adult', 'release_date', 'genres')
    search_fields = ('title', 'description')
    filter_horizontal = ('genres',)  # Better UI for ManyToManyField


@admin.register(MyList)
class MyListAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'user')
    search_fields = ('name', 'slug', 'user__username')
    filter_horizontal = ('movies','shared_with')  # Better UI for ManyToManyField