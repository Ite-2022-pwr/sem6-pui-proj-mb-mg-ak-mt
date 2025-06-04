from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "release_date", "vote_average", "adult")
    list_filter = ("adult", "release_date", "genres")
    search_fields = ("title", "description")
    filter_horizontal = ("genres",)  # Better UI for ManyToManyField


@admin.register(MyList)
class MyListAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    search_fields = ("name", "slug", "user__username")
    filter_horizontal = ("movies", "shared_with")  # Better UI for ManyToManyField


@admin.register(TMDBSettings)
class TMDBSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    readonly_fields = ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        # Ensure only one active configuration
        if obj.is_active:
            TMDBSettings.objects.filter(is_active=True).update(is_active=False)
        super().save_model(request, obj, form, change)
