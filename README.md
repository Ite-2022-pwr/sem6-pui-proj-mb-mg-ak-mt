# sem6-pui-proj-mb-mg-ak-mt
Projekt na Projektowanie usług internetowych

# Setup
## Docker-compose
In [docker-compose.yaml](docker-compose.yaml) we create 3 containers:
```
- moviepicker-backend 
    Django backend exposed on localhost:80000 (currently without https)

- moviepicker-frontend
    Frontend exposed 

- moviepicker-postgres  
    Postgres database with persistent volume (local folder is choosed by docker-compose)
    Exposed on localhost:5432
    So please be aware that your database is not being shared (at least at this moment)
```


To create and run the application run:
`docker-compose up --build`

## Django
When you start Django for the first time (or after database deletion, or after creating new model (doing change in databse)) You need to make migrations to create tables in db.
```
# This will check for any changed to the db and make necessary changes 
docker-compose exec moviepicker-backend python manage.py migrate
docker-compose exec moviepicker-backend python manage.py makemigrations
```

To create an admin user (for admin panel)
```
docker-compose exec moviepicker-backend python manage.py createsuperuser
```


## Import example data
Backend has a cronjob to periodically run the import for 10 TMDB pages. To run it manually run this command:

`docker-compose exec moviepicker-backend python manage.py import_tmdb_data --pages=10 --import-genres`

However you need to have TMDB Settings configured in the django admin panel.

## Deletion / shutting down
To shutdown the containers: `docker-compose down`  

To shutdown the containers and remove everything, volumes, networks:
`docker-compose down --volumes`