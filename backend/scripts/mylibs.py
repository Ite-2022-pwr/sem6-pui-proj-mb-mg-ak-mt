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
        "Authorization": f"Token {MOVIEPICKER_AUTH}"
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
        headers={"Content-Type": "application/json", "Authorization": f"Token {MOVIEPICKER_AUTH}"}
    ).json()

    # Make a request to the TMDB API to get the list of genres
    tmdb_response = requests.get(
        "https://api.themoviedb.org/3/genre/movie/list",
        params={"api_key": TMDB_API_KEY, "language": "en-US"}
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
            headers={"Content-Type": "application/json", "Authorization": f"Token {MOVIEPICKER_AUTH}"}
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
        "Authorization": f"Token {MOVIEPICKER_AUTH}"
    }
    response = requests.delete(
        url,
        headers=headers
    )
    print(response.status_code)
    return response

def genres_delete_by_name(name):
    """
    Deletes a genre by its name using the custom API endpoint.
    """
    url = "http://localhost:8000/api/genres/delete_by_name/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MOVIEPICKER_AUTH}"
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
        "Authorization": f"Token {MOVIEPICKER_AUTH}"
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
        "Authorization": f"Token {MOVIEPICKER_AUTH}"
    }
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    return response

def users_register(username,password,email):
    """
    Register a new user using the /api/auth/register endpoint.
    """
    url = "http://localhost:8000/api/auth/register/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MOVIEPICKER_AUTH}"
    }
    data = {
        "username": username,
        "password": password,
        "email": email
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"Status code: {response.status_code}")
    return response

def users_login(username,password):
    """
    Login user using the /api/auth/login endpoint, returns token.
    """
    response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json={
            "username": f"{username}",
            "password": f"{password}"
        },
        headers={"Content-Type": "application/json"}
    )

    print(f"Status code: {response.status_code}")
    return response

def users_logout(token):
    """
    Logout user using the /api/auth/logout endpoint.
    """
    response = requests.post(
        "http://localhost:8000/api/auth/logout/",

        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {token}"
        },
    )

    print(f"Status code: {response.status_code}")
    return response



### INIT env variables and get aut token ####
load_dotenv()  # Loads .env file into environment
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
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


#TODO: maybe better layout? xD
print(f"MoviePicker auth token: {MOVIEPICKER_AUTH}")