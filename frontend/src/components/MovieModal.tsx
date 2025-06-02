import axios from "axios";
import React, { useState, useEffect } from "react";
import api from "../api";

interface Movie {
  id: number;
  title: string;
  description: string;
  poster_path: string;
  genres: number[];
}

interface Genre {
  id: number;
  name: string;
}

interface MovieList {
  id: number;
  name: string;
  slug: string;
  movies: number[];
}

interface Props {
  movie: Movie;
  onClose: () => void;
}

function MovieModal(props: Props) {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [lists, setLists] = useState<MovieList[]>([]);
  const [chosenList, setChosenList] = useState<MovieList | null>(null);
  const [slug, setSlug] = useState<string | null>(null);

  useEffect(() => {
    const fetchGenres = async () => {
      setSlug(new URLSearchParams(window.location.search).get("slug"));

      try {
        const responseGenres = await api.get<Genre[]>("/genres");
        const filteredGenres = responseGenres.data.filter((genre) =>
          props.movie.genres.includes(genre.id)
        );
        setGenres(filteredGenres);

        const responseLists = await api.get<MovieList[]>("/lists/me");
        setLists(responseLists.data);
        setChosenList(responseLists.data[0]);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          setError(
            `ERROR ${err.response.status}: ${
              err.response.data?.error || "Unknown error"
            }`
          );
        } else {
          setError("Cannot get genres");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchGenres();
  }, []);

  const handleOnChange = (listID: string) => {
    const filteredList = lists.filter((l) => `${l.id}` === listID)[0];
    setChosenList(filteredList);
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();

    chosenList?.movies.push(props.movie.id);

    api
      .post(`/lists/slug/${chosenList?.slug}/`, {
        movie_id: props.movie.id,
      })
      .then(() => {
        alert(`Movie "${props.movie.title}" added to list ${chosenList?.name}`);
        props.onClose();
      })
      .catch((err) => {
        if (axios.isAxiosError(err) && err.response) {
          setError(
            `ERROR ${err.response.status}: ${
              err.response.data?.error || "Unknown error"
            }`
          );
        } else {
          setError("Cannot add to list");
        }
      });
  };

  const removeFromList = () => {
    api
      .delete(`/lists/slug/${slug}/`, {
        data: {
          movie_id: props.movie.id,
        },
      })
      .then(() => {
        alert(`Movie "${props.movie.title}" removed from list`);
        props.onClose();
        window.location.reload();
      })
      .catch((err) => {
        if (axios.isAxiosError(err) && err.response) {
          setError(
            `ERROR ${err.response.status}: ${
              err.response.data?.error || "Unknown error"
            }`
          );
        } else {
          setError("Cannot remove from list");
        }
      });
  };

  const closeModal = (event: React.MouseEvent) => {
    const modalBackground = document.getElementById("movie-modal-bg");
    if (event.target === modalBackground) {
      props.onClose();
    }
  };

  return (
    <div
      id="movie-modal-bg"
      className="fixed top-0 left-0 w-full h-full bg-black/75 flex items-center justify-center z-50 text-mydarkblue"
      onClick={closeModal}
    >
      <div className="bg-mylightgrey dark:bg-mydarkgrey dark:text-mylightgrey rounded-xl flex flex-col gap-6 w-[80%] max-w-2xl h-[80%] overflow-y-auto">
        <form
          id="select-list-form"
          onSubmit={handleSubmit}
          className="p-10 rounded-xl flex flex-col gap-6 max-w-2xl"
        >
          <h1 className="border-b w-full text-4xl">Description</h1>
          <p>{props.movie.description}</p>

          <h1 className="border-b w-full text-4xl">Genres</h1>
          <ul className="list-disc mx-10">
            {genres.map((genre) => {
              return <li key={genre.id}>{genre.name}</li>;
            })}
            {loading && <p className="text-mydarkblue">Loading genres...</p>}
          </ul>

          <h1 className="border-b w-full text-4xl">Add to list</h1>
          <label>
            Choose list:
            <select
              name="lists"
              form="select-list-form"
              onChange={(e) => handleOnChange(e.target.value)}
              className="mx-5 bg-myyellow-1 rounded-2xl p-3 font-bold cursor-pointer text-center text-mydarkblue"
            >
              {lists.map((list) => {
                return (
                  <option
                    key={list.id}
                    className="rounded-lg cursor-pointer"
                    value={list.id}
                  >
                    {list.name}
                  </option>
                );
              })}
            </select>
          </label>
          <button
            type="submit"
            className="bg-mymint w-50 text-black text-xl px-10 py-4 rounded-full font-limelight hover:cursor-pointer hover:bg-green-400"
          >
            Add to list
          </button>
        </form>

        {slug && (
          <div className="p-10 rounded-xl flex flex-col gap-6 max-w-2xl">
            <h1 className="border-b w-full text-4xl"></h1>
            <button
              className="bg-red-400 text-black text-xl px-10 py-4 rounded-full font-limelight hover:cursor-pointer hover:bg-red-500"
              onClick={removeFromList}
            >
              Remove from this list
            </button>
          </div>
        )}

        {error && <p className="text-red-500">{error}</p>}
      </div>
    </div>
  );
}

export default MovieModal;
