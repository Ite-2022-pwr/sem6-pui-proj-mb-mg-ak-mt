from dotenv import load_dotenv
import requests
import os


### Proper helper functions to communicate with api ###
##### GENRES #####
def genres_get_all():
    """
    Fetches and displays all genres from the /api/genres/ endpoint.
    """
    url = "http://localhost:8000/api/genres/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MOVIEPICKER_AUTH}",
    }
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    return response


def genres_import_missing():
    """
    Fetches movie genres from TMDB API and imports only missing to our db.
    """
    our_genre_list = requests.get(
        "http://localhost:8000/api/genres/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {MOVIEPICKER_AUTH}",
        },
    ).json()

    # Make a request to the TMDB API to get the list of genres
    tmdb_response = requests.get(
        "https://api.themoviedb.org/3/genre/movie/list?language=en",
        headers={
            "Authorization": f"Bearer {TMDB_BEARER}",
            "Content-Type": "application/json",
        },
    )
    genres = tmdb_response.json().get("genres", [])

    ### compare 2 jsons list and find missing from the second one
    b_set = {(item["id"], item["name"]) for item in our_genre_list}
    missing = [item for item in genres if (item["id"], item["name"]) not in b_set]
    ###

    if missing:
        django_response = requests.post(
            "http://localhost:8000/api/genres/import/",
            json=missing,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {MOVIEPICKER_AUTH}",
            },
        )
        print(django_response.text)
        return django_response.json()
    else:
        print("No missing genres to import.")
        return {"message": "No missing genres to import."}


def genres_delete_by_id(genre_id):
    """
    Deletes a genre by its ID.
    """
    url = f"http://localhost:8000/api/genres/{genre_id}/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MOVIEPICKER_AUTH}",
    }
    response = requests.delete(url, headers=headers)
    print(response.status_code)
    return response


def genres_delete_by_name(name):
    """
    Deletes a genre by its name using the custom API endpoint.
    """
    url = "http://localhost:8000/api/genres/delete_by_name/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MOVIEPICKER_AUTH}",
    }
    data = {"name": name}

    response = requests.delete(url, headers=headers, json=data)
    print(f"Status code: {response.status_code}")
    return response


##### USERS // AUTHENTICATION #####
def users_show_all():
    """
    Fetches and displays all users from the /api/users/ endpoint.
    """
    url = "http://localhost:8000/api/users/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MOVIEPICKER_AUTH}",
    }
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    return response


def users_show_current():
    """
    Fetches and displays current user info from /api/users/me endpoint.
    """
    url = "http://localhost:8000/api/users/me/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MOVIEPICKER_AUTH}",
    }
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    return response


def users_register(username, password, email):
    """
    Register a new user using the /api/auth/register endpoint.
    """
    url = "http://localhost:8000/api/auth/register/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MOVIEPICKER_AUTH}",
    }
    data = {"username": username, "password": password, "email": email}
    response = requests.post(url, headers=headers, json=data)
    print(f"Status code: {response.status_code}")
    return response


def users_login(username, password):
    """
    Login user using the /api/auth/login endpoint, returns token.
    """
    response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json={"username": f"{username}", "password": f"{password}"},
        headers={"Content-Type": "application/json"},
    )

    print(f"Status code: {response.status_code}")
    return response


def users_logout(token):
    """
    Logout user using the /api/auth/logout endpoint.
    """
    response = requests.post(
        "http://localhost:8000/api/auth/logout/",
        headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
    )

    print(f"Status code: {response.status_code}")
    return response


def movies_list():
    """
    Fetches and displays movies from the /api/movies/ endpoint.
    """
    url = "http://localhost:8000/api/movies/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MOVIEPICKER_AUTH}",
    }
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    return response


def movies_import_new_from_page(page_id):
    """
    Fetches movies from TMDB API for specified page and imports only missing movies to our db.
    """
    headers = {
        "Authorization": f"Token {MOVIEPICKER_AUTH}",
        "Content-Type": "application/json",
    }
    moviepicker_url = "http://localhost:8000/api/movies/import/"
    # api_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={page_id}"

    # Get existing movies (we do not do pagination yet and json returns all movies)
    existing_movies = movies_list().json()
    existing_titles = [
        movie["title"].lower() for movie in existing_movies if "title" in movie
    ]

    print(existing_titles)

    # Get movies from TMDB API
    tmdb_response = requests.get(
        f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page_id}&sort_by=popularity.desc",
        headers={
            "Authorization": f"Bearer {TMDB_BEARER}",
            "Content-Type": "application/json",
        },
    )

    if tmdb_response.status_code != 200:
        print(f"TMDB API request failed: {tmdb_response.status_code}")
        print(tmdb_response.json())
        return
    json_data = tmdb_response.json().get("results", [])

    # 2. Filter out movies that already exist
    to_import = []
    for item in json_data:
        title = item.get("title", "").strip()
        if title.lower() not in existing_titles:
            transformed = {
                "title": title,
                "description": item.get("overview") or "no description provided",
                "poster_path": item.get("poster_path") or ("blank_poster.png"),
                "release_date": item.get("release_date"),
                "vote_average": item.get("vote_average", 0.0),
                "vote_count": item.get("vote_count", 0),
                "adult": item.get("adult", False),
                "genres": item.get("genre_ids", []),
            }
            to_import.append(transformed)

    print(to_import)
    if not to_import:
        print(" No new movies to import.")
        return

    # 3. POST only the new ones
    import_response = requests.post(moviepicker_url, json=to_import, headers=headers)
    if import_response.status_code == 201:
        print(f"Imported {len(to_import)} new movies.")
        return import_response
    else:
        print(f"Import failed: {import_response.status_code}")
        return import_response


### INIT env variables and get aut token ####
load_dotenv()  # Loads .env file into environment
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BEARER = os.getenv("TMDB_BEARER")
MOVIEPICKER_USERNAME = os.getenv("MOVIEPICKER_USERNAME")
MOVIEPICKER_PASSWORD = os.getenv("MOVIEPICKER_PASSWORD")
MOVIEPICKER_AUTH = os.getenv("MOVIEPICKER_AUTH")
MOVIEPICKER_DEV_MODE = os.getenv("MOVIEPICKER_DEV_MODE")
if MOVIEPICKER_DEV_MODE == "True":
    response = users_login(MOVIEPICKER_USERNAME, MOVIEPICKER_PASSWORD)
    if response.status_code == 200:
        MOVIEPICKER_AUTH = response.json().get("token")
    else:
        print("Failed to fetch auth token.")
        MOVIEPICKER_AUTH = None


# TODO: maybe better layout? xD
print(f"MoviePicker auth token: {MOVIEPICKER_AUTH}")
