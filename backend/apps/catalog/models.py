from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


# TODO: Maybe optimize the field types
class Movie(models.Model):
    title = models.CharField(max_length=254)
    description = models.TextField()
    poster_path = models.TextField()
    release_date = models.DateTimeField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    adult = models.BooleanField()
    genres = models.ManyToManyField(
        Genre, related_name="movies"
    )  # Related name to be able to access via genre.movies.all()

    class Meta:
        db_table = "catalog_movie"

    def __str__(self):
        return self.title


class MyList(models.Model):
    DEFAULT_LISTS = ["watched", "favorites", "to_watch"]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_lists")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    movies = models.ManyToManyField("Movie", related_name="my_lists")

    shared_with = models.ManyToManyField(User, related_name="shared_lists", blank=True)

    class Meta:
        unique_together = ("user", "slug")
        db_table = "mylist"

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    # Autmatically generate a slug for the list name and make sure they are unique
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1
            while MyList.objects.filter(user=self.user, slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)


class TMDBSettings(models.Model):
    api_key = models.CharField(max_length=255, help_text="TMDB API Key")
    bearer_token = models.TextField(help_text="TMDB Bearer Token")
    base_url = models.URLField(
        default="https://api.themoviedb.org/3/", help_text="TMDB API Base URL"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True, help_text="Whether this configuration is active"
    )

    class Meta:
        db_table = "tmdb_settings"
        verbose_name = "TMDB Settings"
        verbose_name_plural = "TMDB Settings"

    def __str__(self):
        return f"TMDB Settings (Active: {self.is_active})"

    @classmethod
    def get_active_settings(cls):
        """Get the active TMDB settings"""
        return cls.objects.filter(is_active=True).first()
