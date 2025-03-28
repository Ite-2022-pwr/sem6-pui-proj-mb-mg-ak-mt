# sem6-pui-proj-mb-mg-ak-mt
Projekt na Projektowanie usług internetowych

# Setup
## Docker-compose
Currently in [docker-compose.yaml](docker-compose.yaml) we create 2 containers:
    - moviepicker-backend 
        Django backend exposed on localhost:80000 (currently without https)
    - moviepicker-postgres -- 
        Postgres database with persistent volume (local folder is choosed by docker-compose)
        Exposed on localhost:5432



To create and run the application run:
`docker-compose up --build`