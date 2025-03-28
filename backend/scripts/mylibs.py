from dotenv import load_dotenv
import requests
import os

load_dotenv()  # Loads .env file into environment

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


def import_missing_genres():

    """
    Fetches movie genres from TMDB API and imports only missing to our db.
    """
    our_genre_list = requests.get(
        "http://localhost:8000/api/genres/",
        headers={"Content-Type": "application/json"}
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