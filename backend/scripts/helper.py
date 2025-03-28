import argparse
import typer

from mylibs import *

app = typer.Typer()
genres_app = typer.Typer(help="Genre-related commands like import and delete.")
movies_app = typer.Typer()

app.add_typer(genres_app, name="genres")
app.add_typer(movies_app, name="movies")

@genres_app.command("import_missing")
def import_missing():
    import_missing_genres()

@genres_app.command("delete_id")
def delete_by_id(id: int = typer.Argument(..., help="The ID of the genre to delete.")):
    delete_genre_by_id(id)

@movies_app.command("list")
def list_():
    pass
    # list_movies()

if __name__ == "__main__":
    app()




