from dotenv import load_dotenv
import requests
import os

load_dotenv()  # Loads .env file into environment




def get_moviepicker_auth_token():
    """
    Fetches the MoviePicker authentication token from the API.
    """
    response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json={
            "username": "admin",
            "password": "admin"
        },
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        token = response.json().get("token")
        return token
    else:
        print("Failed to fetch auth token.")
        return None

#TODO: maybe better layout? xD
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
moviepicker_auth_token = os.getenv("MOVIEPICKER_AUTH_TOKEN")
if not moviepicker_auth_token:
    moviepicker_auth_token = get_moviepicker_auth_token()
print(f"MoviePicker auth token: {moviepicker_auth_token}")



def import_missing_genres():

    """
    Fetches movie genres from TMDB API and imports only missing to our db.
    """
    our_genre_list = requests.get(
        "http://localhost:8000/api/genres/",
        headers={"Content-Type": "application/json", "Authorization": f"Token {moviepicker_auth_token}"}
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
            headers={"Content-Type": "application/json"}
        )
        print(django_response.text)
        return django_response.json()
    else:
        print("No missing genres to import.") 
        return {"message": "No missing genres to import."}
    
def delete_genre_by_id(genre_id):
    """
    Deletes a genre by its ID.
    """
    response = requests.delete(
        f"http://localhost:8000/api/genres/{genre_id}/",
        headers={"Content-Type": "application/json"}
    )
    print(response.status_code)
    return response



