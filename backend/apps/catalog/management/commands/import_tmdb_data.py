from django.utils import timezone
from apps.catalog.models import TMDBSettings, Genre, Movie
from django.core.management.base import BaseCommand
from apps.catalog.serializers import MovieSerializer
import requests
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import movies and genres from TMDB automatically"

    def add_arguments(self, parser):
        parser.add_argument(
            "--pages",
            type=int,
            default=5,
            help="Number of pages to import from TMDB (default: 5)",
        )
        parser.add_argument(
            "--import-genres", action="store_true", help="Also import missing genres"
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(f"Starting TMDB import at {timezone.now()}")
        )

        try:
            # Get TMDB settings
            tmdb_settings = TMDBSettings.get_active_settings()
            if not tmdb_settings:
                self.stdout.write(self.style.ERROR(
                    "No active TMDB settings found."))
                return

            # Import genres if requested
            if options["import_genres"]:
                self.import_missing_genres(tmdb_settings)

            # Import movies
            pages_to_import = options["pages"]
            self.import_movies_from_pages(tmdb_settings, pages_to_import)

            self.stdout.write(
                self.style.SUCCESS(
                    f"TMDB import completed at {timezone.now()}")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"TMDB import failed: {str(e)}"))
            logger.error(f"TMDB import failed: {str(e)}", exc_info=True)

    def import_missing_genres(self, tmdb_settings):
        """Import missing genres from TMDB"""
        self.stdout.write("Importing missing genres...")

        # Get existing genres
        existing_genres = Genre.objects.all()
        existing_set = {(genre.id, genre.name) for genre in existing_genres}

        # Fetch from TMDB
        response = requests.get(
            f"{tmdb_settings.base_url.rstrip('/')}/genre/movie/list",
            headers={
                "Authorization": f"Bearer {tmdb_settings.bearer_token}",
                "Content-Type": "application/json",
            },
            params={"language": "en"},
        )
        response.raise_for_status()

        tmdb_genres = response.json().get("genres", [])
        missing_genres = [
            genre
            for genre in tmdb_genres
            if (genre["id"], genre["name"]) not in existing_set
        ]

        imported_count = 0
        for genre_data in missing_genres:
            if not Genre.objects.filter(id=genre_data["id"]).exists():
                Genre.objects.create(
                    id=genre_data["id"], name=genre_data["name"])
                imported_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Imported {imported_count} new genres"))

    def import_movies_from_pages(self, tmdb_settings, num_pages):
        """Import movies from multiple TMDB pages"""
        self.stdout.write(f"Importing movies from {num_pages} pages...")

        total_imported = 0
        existing_titles = set(Movie.objects.values_list(
            "title", flat=True).iterator())

        for page in range(1, num_pages + 1):
            self.stdout.write(f"Processing page {page}...")

            response = requests.get(
                f"{tmdb_settings.base_url.rstrip('/')}/discover/movie",
                headers={
                    "Authorization": f"Bearer {tmdb_settings.bearer_token}",
                    "Content-Type": "application/json",
                },
                params={
                    "include_adult": "false",
                    "include_video": "false",
                    "language": "en-US",
                    "page": page,
                    "sort_by": "popularity.desc",
                },
            )
            response.raise_for_status()

            tmdb_movies = response.json().get("results", [])
            page_imported = 0

            for movie_data in tmdb_movies:
                title = movie_data.get("title", "").strip()
                if not title or title in existing_titles:
                    continue

                # Transform data
                transformed = {
                    "title": title,
                    "description": movie_data.get("overview")
                    or "No description provided",
                    "poster_path": movie_data.get("poster_path") or "blank_poster.png",
                    "release_date": movie_data.get("release_date"),
                    "vote_average": movie_data.get("vote_average", 0.0),
                    "vote_count": movie_data.get("vote_count", 0),
                    "adult": movie_data.get("adult", False),
                    "genres": movie_data.get("genre_ids", []),
                }

                serializer = MovieSerializer(data=transformed)
                if serializer.is_valid():
                    serializer.save()
                    existing_titles.add(title)
                    page_imported += 1
                    total_imported += 1

            self.stdout.write(f"Page {page}: imported {page_imported} movies")

        self.stdout.write(
            self.style.SUCCESS(f"Total imported: {total_imported} movies")
        )
