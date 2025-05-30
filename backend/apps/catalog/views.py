from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# TODO: Add authentication

# This is dirty fix to get the next available ID if we want to import genre name without ID
# TODO: Talk with others if we want this or not. If not, then we always need to specify
#       the id ourselves.


def reset_genre_id_sequence():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT setval(pg_get_serial_sequence('catalog_genre', 'id'), (SELECT MAX(id) FROM catalog_genre));"
        )


def reset_movie_id_sequence():
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT setval(pg_get_serial_sequence('catalog_movie', 'id'), (SELECT MAX(id) FROM catalog_movie));"
        )


# TODO: Review urls/paths here
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    delete_by_name_request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(
                type=openapi.TYPE_STRING, description="Name of the genre to delete"
            )
        },
        required=["name"],
        example={"name": "Genre_name"},
    )

    @swagger_auto_schema(request_body=delete_by_name_request_body)
    @action(detail=False, methods=["delete"], url_path="delete_by_name")
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
            return Response(
                {"error": "Missing 'name' in request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            genre = Genre.objects.get(name=name)
            genre.delete()

            return Response(
                {"message": f"Genre '{name}' deleted."}, status=status.HTTP_200_OK
            )
        except Genre.DoesNotExist:
            return Response(
                {"error": f"Genre '{name}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    ########### POST -- BULK IMPORT ##################
    # Define the schema for a single genre item.
    genre_item_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Optional custom genre ID"
            ),
            "name": openapi.Schema(
                type=openapi.TYPE_STRING, description="Name of the genre"
            ),
        },
        required=["name"],  # 'name' is required; 'id' is optional.
    )
    # Define the schema for the entire request body (a list of genre items) and add an example.
    import_genres_schema = openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=genre_item_schema,
        example=[{"id": 4, "name": "test-id-4"}, {"name": "test-without-id"}],
    )

    @swagger_auto_schema(request_body=import_genres_schema)
    @action(detail=False, methods=["post"], url_path="import")
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
            return Response({"error": "Expected a list of genre objects."}, status=400)

        imported = []
        for item in data:
            genre_id = item.get("id")
            name = item.get("name")

            # Validate required fields
            if name is None:
                return Response(
                    {
                        "error": f"Each item must include 'name'. Problematic entry: {item}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if ID or name already exists
            if Genre.objects.filter(id=genre_id).exists():
                return Response(
                    {"error": f"Genre with ID {genre_id} already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if Genre.objects.filter(name=name).exists():
                return Response(
                    {"error": f"Genre with name '{name}' already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
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

        return Response({"imported": imported}, status=status.HTTP_201_CREATED)


#### MOVIES #####
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    ########## DELETE by title ##########
    # Define the request body schema for deleting by title.
    delete_by_title_request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(
                type=openapi.TYPE_STRING, description="Title of the movie to delete"
            )
        },
        required=["title"],
        example={"title": "Movie Title"},
    )

    @swagger_auto_schema(
        request_body=delete_by_title_request_body,
        responses={
            200: openapi.Response(
                description="Movie deleted successfully",
                examples={
                    "application/json": {"message": "Movie 'Movie Title' deleted."}
                },
            ),
            404: openapi.Response(
                description="Movie not found",
                examples={
                    "application/json": {"error": "Movie 'Movie Title' not found."}
                },
            ),
            400: openapi.Response(
                description="Missing title in request body",
                examples={
                    "application/json": {"error": "Missing 'title' in request body."}
                },
            ),
        },
    )
    @action(detail=False, methods=["delete"], url_path="delete_by_title")
    def delete_by_title(self, request):
        """
        Delete a movie by title.
        Requires auth token in header.
        Expected JSON body
        {
            "title": "Movie Title"
        }
        Returns
            - 200 if deleted
            - 404 if not found
        """
        title = request.data.get("title")

        if not title:
            return Response(
                {"error": "Missing 'title' in request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            movie = Movie.objects.get(title=title)
            movie.delete()
            return Response(
                {"message": f"Movie '{title}' deleted."}, status=status.HTTP_200_OK
            )
        except Movie.DoesNotExist:
            return Response(
                {"error": f"Movie '{title}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    ########## BULK IMPORT ##########
    @action(detail=False, methods=["post"], url_path="import")
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
            return Response({"error": "Expected a list of movie objects."}, status=400)

        imported = []

        for item in data:
            movie_id = item.get("id")
            title = item.get("title")
            release_date = item.get("release_date")
            genres = item.get("genres")

            if not title or not release_date or not genres:
                return Response(
                    {
                        "error": f"must include 'title', 'release_date', and 'genres' {item}"
                    },
                    status=400,
                )

            if Movie.objects.filter(id=movie_id).exists():
                return Response(
                    {"error": f"Movie with ID {movie_id} already exists."}, status=400
                )
            if Movie.objects.filter(title=title).exists():
                return Response(
                    {"error": f"Movie '{title}' already exists."}, status=400
                )

            serializer = MovieSerializer(data=item)
            if not serializer.is_valid():
                return Response({"error": serializer.errors, "item": item}, status=400)

            movie = serializer.save()
            imported.append(MovieSerializer(movie).data)

        reset_movie_id_sequence()

        return Response({"imported": imported}, status=201)


#### LISTS #####


class MyListViewSet(viewsets.ModelViewSet):
    """
    Get /lists/ requires being admin
    To get lists for current user, go to /lists/me
    To create list, do a POST request to /lists/
    """

    serializer_class = MyListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Admins can see all lists; others see nothing here by default.
        """
        user = self.request.user
        if user.is_staff:
            return MyList.objects.all()
        return MyList.objects.none()

    def get_object(self):
        """
        Override get_object to allow users to access lists they own or are shared with.
        This enables GET/PATCH/DELETE operations on /api/lists/<id>/
        """
        # Get the object ID from the URL
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]

        try:
            obj = MyList.objects.get(pk=lookup_value)
        except MyList.DoesNotExist:
            from django.http import Http404

            raise Http404("List not found")

        user = self.request.user

        # Allow access if user is admin, owner, or shared user
        if user.is_staff or obj.user == user or user in obj.shared_with.all():
            return obj

        # If user doesn't have permission, raise 404 instead of 403 for security
        from django.http import Http404

        raise Http404("List not found")

    def perform_update(self, serializer):
        """
        Only allow list owners and admins to update lists.
        """
        list_obj = self.get_object()
        if self.request.user != list_obj.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Only the list owner or admin can modify this list.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Only allow list owners and admins to delete lists.
        Returns a proper response for DELETE operations.
        """
        if self.request.user != instance.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Only the list owner or admin can delete this list.")

        list_name = instance.name
        instance.delete()

        # Return a proper success response
        return Response(
            {"message": f"List '{list_name}' deleted successfully."},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to return a proper response instead of 204 No Content.
        """
        instance = self.get_object()
        if self.request.user != instance.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Only the list owner or admin can delete this list.")

        list_name = instance.name
        instance.delete()

        return Response(
            {"message": f"List '{list_name}' deleted successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="me")
    def my_lists(self, request):
        """
        Returns lists owned by or shared with the current user.
        GET /api/lists/me/
        """
        user = request.user
        queryset = MyList.objects.filter(user=user) | MyList.objects.filter(
            shared_with=user
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Automatically assign the current user as the owner when creating a list.
        """
        serializer.save(user=self.request.user)

    @action(
        detail=False, methods=["post", "delete"], url_path="slug/(?P<slug>[^/]+)/share"
    )
    def share_by_slug(self, request, slug=None):
        """
        Share or unshare a list by slug with another user.

        ### POST
        Share a list with a user:
        URL:   /api/lists/slug/<slug>/share/
        Body:  { "username": "friend_username" }

        ### DELETE
        Unshare a list from a user:
        URL:   /api/lists/slug/<slug>/share/
        Body:  { "username": "friend_username" }

        Returns:
            - 200 OK on success
            - 400 if input is missing
            - 403 if user is not the list owner
            - 404 if user or list not found
        """
        try:
            list_obj = MyList.objects.get(slug=slug)
        except MyList.DoesNotExist:
            return Response({"error": "List not found"}, status=404)

        if request.user != list_obj.user:
            return Response({"error": "You do not own this list."}, status=403)

        username = request.data.get("username")
        if not username:
            return Response({"error": 'Missing "username"'}, status=400)

        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if request.method == "POST":
            list_obj.shared_with.add(target_user)
            return Response({"message": f"List '{slug}' shared with {username}."})

        elif request.method == "DELETE":
            list_obj.shared_with.remove(target_user)
            return Response({"message": f"List '{slug}' unshared from {username}."})

        return Response({"error": "Method not allowed."}, status=405)

    delete_movies_request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "movie_ids": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_INTEGER),
                description="List of movie IDs to remove",
            )
        },
        required=["movie_ids"],
        example={"movie_ids": [5, 7, 9]},
    )

    @swagger_auto_schema(method="delete", request_body=delete_movies_request_body)
    @action(
        detail=False, methods=["get", "post", "delete"], url_path="slug/(?P<slug>[^/]+)"
    )
    def handle_list_by_slug(self, request, slug=None):
        """
        Handler for interacting with a list by its slug
        ## Supports
        - GET    /api/lists/slug/{slug}/      → Returns list details
        - POST   /api/lists/slug/{slug}/      → Adds movie(s) to the list
        - DELETE /api/lists/slug/{slug}/      → Removes movie(s) from the list
        ## Permissions
        - User must be the list owner or one of the shared users.
        ## POST & DELETE Payloads:
        Accepts either a single movie ID:
            `{ "movie_id": 5 }`
        Or a list of movie IDs:
            `{ "movie_ids": [5, 7, 9] }`
        ## Returns
            - 200 OK with a success message or list details
            - 403 Forbidden if user doesn't have access
            - 404 Not Found if list or movie does not exist
            - 400 Bad Request if input is missing or invalid
        """
        try:
            # First try to find a list owned by the current user
            list_obj = MyList.objects.get(slug=slug, user=request.user)
        except MyList.DoesNotExist:
            # If not found, try to find a list shared with the current user
            try:
                list_obj = MyList.objects.get(slug=slug, shared_with=request.user)
            except MyList.DoesNotExist:
                return Response(
                    {"error": f"List not found, current user {request.user}"},
                    status=404,
                )

        if (
            request.user != list_obj.user
            and request.user not in list_obj.shared_with.all()
        ):
            return Response({"error": "Permission denied."}, status=403)

        if request.method == "GET":
            serializer = self.get_serializer(list_obj)
            return Response(serializer.data)

        # Get movie IDs from request (accept single int or list)
        movie_ids = request.data.get("movie_id") or request.data.get("movie_ids")

        if not movie_ids:
            return Response({"error": "Missing movie_id(s)"}, status=400)

        if isinstance(movie_ids, int):
            movie_ids = [movie_ids]  # Wrap single ID in a list

        if not isinstance(movie_ids, list):
            return Response(
                {"error": "movie_ids must be a list of integers."}, status=400
            )

        # Fetch valid movie objects
        movies = list(Movie.objects.filter(id__in=movie_ids))
        found_ids = {m.id for m in movies}
        missing_ids = set(movie_ids) - found_ids

        if request.method == "POST":
            list_obj.movies.add(*movies)
            msg = f"Added {len(movies)} movie(s) to list '{slug}'."
            if missing_ids:
                msg += f" Skipped missing IDs: {list(missing_ids)}"
            return Response({"message": msg})

        elif request.method == "DELETE":
            list_obj.movies.remove(*movies)
            msg = f"Removed {len(movies)} movie(s) from list '{slug}'."
            if missing_ids:
                msg += f" Skipped missing IDs: {list(missing_ids)}"
            return Response({"message": msg})

        return Response({"error": "Method not allowed."}, status=405)
