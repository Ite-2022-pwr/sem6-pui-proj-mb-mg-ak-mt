# MoviePicker backend
admin gui:
http://localhost:8000/admin/


## Implemented:
### Genres
url: /api/genres/
functions:
- Bulk import from json
- Delete by ID 
- Delete by Name
- Get JSON with all genres  


url: /api/genres -- [GET] get all genres   
url: /api/genres/<ID> -- [DELETE] (without body) Delete genre with specific ID  
url: /api/genres/delete_by_name/ -- [DELETE] Delete genre with specific ID  
url: /api/genres/import_genres -- [POST] Insert genres from json  


### Authentication
url: /api/auth/login -- [POST] pass creds to get auth token  
url: /api/auth/logout -- [POST] pass token to logout  
url: /api/auth/register -- [POST] pass username,email,password to create user. 
It also automatically creates 3 lists for user  [Recommended,Watched,Favorites]


### Users
url: /api/users/ -- [GET] get all users  
url: /api/users/me -- [GET] get info about current user  

### Movies
url /api/movies/ -- [GET] get all movies  
url /api/movies/ -- [POST] Create a single movie entry  
url /api/movies/<id>/ -- [DELETE] delete movie with specific ID
url /api/movies/<id>/ -- [PATCH] update movie with specific ID (with json ofc)
url /api/movies/import -- [POST] bulk import movies from json  

### Lists
Slug is created by converting the list name to URL friendly string with user_id in the beggining.
For example user with ID 1 creates "Awesome list", slug will be: "1-awesome_list"
url: /api/lists -- [GET] Requires admin, returns all lists for all users
url: /api/lists/me -- [GET] get all lists for current user
url: /api/lists -- [POST] Create new list from json (name is required, movies and shared_with are optional)
url: /api/lists/slug/<slug> -- [GET] Get a list with specific slug
url: /api/lists/slug/<slug> -- [POST] Add a single or list of movies to  list
url: /api/lists/slug/<slug> -- [DELETE] Delete a single or list of movies to  list
url: /api/lists/slug/<slug>/share -- [POST] -- Share a list with other user (requires username in body ) 
url: /api/lists/slug/<slug>/share -- [DELETE] -- Unshare a list with other user (requires username in body ) 

## Helper scripts
In oder to use `helper.py`, you need to have `requests, typer` installed and you need to create `.env` file with:

```
TMDB_API_KEY=<TMDB_API_KEY>  
MOVIEPICKER_USERNAME=<django_admin_username>  
MOVIEPICKER_PASSWORD=<dhango_admin_password>  
MOVIEPICKER_DEV_MODE=True # If this is set to True, then the app will automatically get the token from the backend  
MOVIEPICKER_AUTH=test_token # If DEV_MODE=false, you need to set token here from /api/auth/login after logging in  
```

#### Import genres from the TMDB:
`py helper.py genres import_missing`

#### Import movies from TMDB page id (they are sorted by popularity)
`py backend/scripts/helper.py movies import_page <id>`

#TODO: Create scripts to create users
