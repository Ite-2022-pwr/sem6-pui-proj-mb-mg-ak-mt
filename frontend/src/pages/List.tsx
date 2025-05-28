import axios from "axios";
import api from "../api";
import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import MovieCard from "../components/MovieCard";

interface MovieList {
  id: number;
  name: string;
  slug: string;
  movies: number[];
}

interface Movie {
  id: number;
  title: string;
  description: string;
  poster_path: string;
  genres: number[];
}

function List() {
  const [listName, setListName] = useState<string | null>("");
  const [movies, setMovies] = useState<Movie[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const listSlug = new URLSearchParams(window.location.search).get("slug");

    const fetchMovies = async () => {
      try {
        const responseList = await api.get<MovieList>(
          `/lists/slug/${listSlug}`
        );

        setListName(responseList.data.name);

        const listMovies: Movie[] = [];

        for (const id of responseList.data.movies) {
          const res = await api.get<Movie>(`/movies/${id}`);
          listMovies.push(res.data);
        }

        setMovies(listMovies);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          setError(
            `ERROR ${err.response.status}: ${
              err.response.data?.message || "Unknown error"
            }`
          );
        } else {
          setError("Cannot get movies");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, []);

  return (
    <>
      <Navbar />
      <div className="bg-mywhite min-h-screen px-8 py-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-mydarkblue text-3xl font-limelight border-b w-fit">
            My lists &gt; {listName}
          </h2>
          <input
            type="text"
            placeholder="Search"
            className="rounded-full px-4 py-1 bg-myyellow-1 text-mydarkblue placeholder-mydarkblue focus:outline-none w-48"
          />
        </div>

        {loading && <p className="text-mydarkblue">Loading movies...</p>}
        {error && <p className="text-red-500">{error}</p>}

        <div className="flex flex-wrap gap-6 text-mydarkblue font-serif text-2xl text-wrap">
          {movies.map((movie) => {
            return <MovieCard key={movie.id} movie={movie} />;
          })}
        </div>

        {!movies.length && (
          <p className="my-20 font-bold text-2xl">No movies on this list</p>
        )}
      </div>
    </>
  );
}

export default List;
