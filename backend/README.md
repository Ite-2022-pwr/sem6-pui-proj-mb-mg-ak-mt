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


## Helper scripts
In oder to use `helper.py`, you need to have `requests, typer` installed and you need to create `.env` file with:
`TMDB_API_KEY=<TMDB_API_KEY>`
#### Import genres from the TMDB:
`py helper.py genres import_missing`