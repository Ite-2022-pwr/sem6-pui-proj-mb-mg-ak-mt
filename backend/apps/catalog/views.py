from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection

# TODO: Add authentication

# This is dirty fix to get the next available ID if we want to import genre name without ID
# TODO: Talk with others if we want this or not. If not, then we always need to specify
#       the id ourselves.
def reset_genre_id_sequence():
    with connection.cursor() as cursor:
        cursor.execute("SELECT setval(pg_get_serial_sequence('catalog_genre', 'id'), (SELECT MAX(id) FROM catalog_genre));")

def reset_movie_id_sequence():
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT setval(pg_get_serial_sequence('catalog_movie', 'id'), (SELECT MAX(id) FROM catalog_movie));")


# TODO: Review urls/paths here
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
  
    @action(detail=False, methods=['delete'], url_path='delete_by_name')
    def delete_by_name(self, request):
        """
        Single Delete a genre by name.
        Requires auth token in header

        Expected JSON body:
        ```
        {
            "name": "Genre_name"
        }
        ```

        ### Returns:
        ```
            - 200 Resource deleted.
            - 404 Resource not found
        ```
            
        ### Examples:
        #### DELETE using the id 
        `curl -X DELETE -H "Authorization: Token <token>" http://localhost:8000/api/genres/<ID>/`

        #### DELETE using the name
        `curl -X DELETE -H "Authorization: Token <token>" http://localhost:8000/api/genres/delete_by_name/ -H "Content-Type: application/json" -d '{"name": "test-id-5"}'`


        """
        name = request.data.get("name")

        if not name:
            return Response({"error": "Missing 'name' in request body."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            genre = Genre.objects.get(name=name)
            genre.delete()

            return Response({"message": f"Genre '{name}' deleted."}, status=status.HTTP_200_OK)
        except Genre.DoesNotExist:
            return Response({"error": f"Genre '{name}' not found."}, status=status.HTTP_404_NOT_FOUND)



########### POST -- BULK IMPORT ##################
    @action(detail=False, methods=['post'], url_path='import')
    def import_genres(self, request):
        """
        Bulk import genres using custom IDs.
        Expects auth token in header.

        Expected JSON input:
        ```
        [
            {"id": 28, "name": "Action"},
            {"name": "Comedy"}
        ]
        ```

        - Creates each genre with the specified ID and name.
        - Returns an error if any ID or name already exists.
        - !!!Does not allow partial success!!! — the whole batch fails if one item is invalid.
        - Allows for imports with only names, then it will use next-after-max ID

        ### Returns:
            201 Created on success with imported genres.
            400 Bad Request if input is invalid or any genre already exists.

        ### Examples:
        ```
        curl -X POST http://localhost:8000/api/genres/import/ \
        -H "Content-Type: application/json" \
        -H "Authorization: Token <token>" \
        -d '[
            {"id":4, "name": "test-id-4"},
            {"name": "test-without-id"}
        ]'
        ```
        """
        data = request.data

        if not isinstance(data, list):
            return Response({'error': 'Expected a list of genre objects.'}, status=400)

        imported = []
        for item in data:
            genre_id = item.get("id")
            name = item.get("name")

            # Validate required fields
            if  name is None:
                return Response(
                    {"error": f"Each item must include 'name'. Problematic entry: {item}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if ID or name already exists
            if Genre.objects.filter(id=genre_id).exists():
                return Response(
                    {"error": f"Genre with ID {genre_id} already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if Genre.objects.filter(name=name).exists():
                return Response(
                    {"error": f"Genre with name '{name}' already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the genre with the custom ID if possible if not, auto-generate id
            if genre_id is not None:
                genre = Genre(id=genre_id, name=name)
            else:
                genre = Genre(name=name)
            genre.save()
            imported.append(GenreSerializer(genre).data)
        # Reset DB last index to current maximum available
        reset_genre_id_sequence()

        return Response({'imported': imported}, status=status.HTTP_201_CREATED)



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    ########## DELETE by title ##########
    @action(detail=False, methods=['delete'], url_path='delete_by_title')
    def delete_by_title(self, request):
        """
        Delete a movie by title.
        Requires auth token in header.

        Expected JSON body:
        {
            "title": "Movie Title"
        }

        Returns:
            - 200 if deleted
            - 404 if not found
        """
        title = request.data.get("title")

        if not title:
            return Response({"error": "Missing 'title' in request body."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(title=title)
            movie.delete()
            return Response({"message": f"Movie '{title}' deleted."}, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({"error": f"Movie '{title}' not found."}, status=status.HTTP_404_NOT_FOUND)

    ########## BULK IMPORT ##########
    @action(detail=False, methods=['post'], url_path='import')
    def import_movies(self, request):
        """
        Bulk import movies with optional custom IDs.
        Requires auth token.

        Expected JSON input:
        [
            {
                "id": 101,
                "title": "Dune",
                "description": "Epic sci-fi...",
                "poster_path": "/img/dune.jpg",
                "release_date": "2021-10-22T00:00:00Z",
                "vote_average": 8.2,
                "vote_count": 1500,
                "adult": false,
                "genres": [1, 2]
            },
            ...
        ]

        - All movies must include at least: title, release_date, and genres.
        - Fails completely on any invalid item.
        - Resets auto-increment ID after import.
        """
        data = request.data

        if not isinstance(data, list):
            return Response({'error': 'Expected a list of movie objects.'}, status=400)

        imported = []

        for item in data:
            movie_id = item.get("id")
            title = item.get("title")
            release_date = item.get("release_date")
            genres = item.get("genres")

            if not title or not release_date or not genres:
                return Response(
                    {"error": f"Each item must include 'title', 'release_date', and 'genres'. Problematic entry: {item}"},
                    status=400
                )

            if Movie.objects.filter(id=movie_id).exists():
                return Response({"error": f"Movie with ID {movie_id} already exists."}, status=400)
            if Movie.objects.filter(title=title).exists():
                return Response({"error": f"Movie '{title}' already exists."}, status=400)

            serializer = MovieSerializer(data=item)
            if not serializer.is_valid():
                return Response({"error": serializer.errors, "item": item}, status=400)

            movie = serializer.save()
            imported.append(MovieSerializer(movie).data)

        reset_movie_id_sequence()

        return Response({'imported': imported}, status=201)