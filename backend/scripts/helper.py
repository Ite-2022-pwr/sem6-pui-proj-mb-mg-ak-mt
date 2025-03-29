import argparse
import typer

from mylibs import *

app = typer.Typer()
genres_app = typer.Typer(help="Genre-related commands like import and delete.")
movies_app = typer.Typer(help=" Movies To be implemented")
series_app = typer.Typer(help=" Series To be implemented")
users_app = typer.Typer(help="Commands related to users and authentication.")

app.add_typer(genres_app, name="genres")
app.add_typer(movies_app, name="movies")
app.add_typer(series_app, name="series")
app.add_typer(users_app, name="users")


##### GENRES #####
@genres_app.command("get_all", help="Show all genres, requires logged in")
def genresapp_get_all():
    print(genres_get_all().json())
@genres_app.command("delete_id", help="Delete a genre by ID, requires admin")
def genresapp_delete_by_id(id: int = typer.Argument(..., help="The ID of the genre to delete.")):
    print(genres_delete_by_id(id).json())
@genres_app.command("delete_name", help="Delete a genre by name, requires admin")
def genresapp_delete_by_name(name: str = typer.Argument(..., help="The name of the genre to delete.")):
    print(genres_delete_by_name(name).json())

@genres_app.command("import_missing", help="Import missing genres from TMDB, requires admin")
def genresapp_import_missing():
    print(genres_import_missing().json())


##### USERS // AUTHENTICATION #####
@users_app.command("show_all", help="Get all users from /api/users/ endpoint, requires admin")
def usersapp_show_all():
    print(users_show_all().json())

@users_app.command("show_current", help="Get current user info  from /api/users/me endpoint, requires logged in")
def usersapp_show_current():
    print(users_show_current().json())

@users_app.command("register", help="Register new user with /api/auth/register endpoint")
def usersapp_register(
    username: str = typer.Argument(..., help="Username for the new user"),
    password: str = typer.Argument(..., help="Password for the new user"),
    email: str = typer.Argument(..., help="Email address for the new user")
    ):
        print(users_register(username,password,email).json())

@users_app.command("login", help="Login user with /api/auth/login endpoint, returns auth token,requires username and password")
def usersapp_login(
    username: str = typer.Argument(..., help="Username "),
    password: str = typer.Argument(..., help="Password ")
    ):
        print(users_login(username,password).json())

@users_app.command("logout", help="Logout user with /api/auth/logout endpoint, ")
def usersapp_logout(
    token: str = typer.Argument(..., help="Auth token ")
    ):
        print(users_logout(token).json())



### MOVIES #####
@movies_app.command("list", help=" To be implemented")
def moviesapp_list():
    pass
    # list_movies()

### SERIES #####
@series_app.command("list", help=" To be implemented")
def seriesapp_list_():
    pass



if __name__ == "__main__":
    app()




