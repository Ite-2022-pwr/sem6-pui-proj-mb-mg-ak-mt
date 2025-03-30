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
url: /api/auth/register -- [POST] pass username,email,password to create user  


### Users
url: /api/users/ -- [GET] get all users  
url: /api/users/me -- [GET] get info about current user  

### Movies
url /api/movies -- [GET] get all movies  
url /api/movies/<id>/ -- [DELETE] delete movie with specific ID
url /api/movies/<id>/ -- [PATCH] update movie with specific ID (with json ofc)
url /api/movies/import -- [POST] import movies from json  


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
