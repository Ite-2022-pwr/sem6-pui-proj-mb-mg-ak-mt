import axios from "axios";
import { useEffect, useState } from "react";
import api from "../api";
import Navbar from "../components/Navbar";
import MovieCard from "../components/MovieCard";
import DeleteListButton from "../components/DeleteListButton";
import ShareListButton from "../components/ShareListButton";
import SearchBar from "../components/SearchBar";
import ErrorAlert from "../components/ErrorAlert";

interface MovieList {
  id: number;
  name: string;
  slug: string;
  movies: number[];
  shared_with: number[];
}

interface Movie {
  id: number;
  title: string;
  description: string;
  poster_path: string;
  genres: number[];
}

function List() {
  const [list, setList] = useState<MovieList>({
    id: -1,
    name: "",
    slug: "",
    movies: [],
    shared_with: [],
  });
  const [listName, setListName] = useState<string | null>("");
  const [listID, setListID] = useState<number>(-1);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<{
    status?: number;
    message: string;
  } | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");

  useEffect(() => {
    const fetchMovies = async () => {
      const listSlug = new URLSearchParams(window.location.search).get("slug");

      try {
        const responseList = await api.get<MovieList>(
          `/lists/slug/${listSlug}`
        );
        const { id, name, movies: movieIds } = responseList.data;

        setList(responseList.data);
        setListID(id);
        setListName(name);

        const movieResponses = await Promise.all(
          movieIds.map((id) => api.get<Movie>(`/movies/${id}`))
        );

        setMovies(movieResponses.map((res) => res.data));
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          setError({
            status: err.response.status,
            message: err.response.data?.error || "Unknown error",
          });
        } else {
          setError({ message: "Cannot get movies" });
        }
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, []);

  const filteredMovies = movies.filter((movie) =>
    movie.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Navbar />

      <div className="bg-mylightgrey dark:bg-mydarkgrey min-h-screen px-8 py-4">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 gap-2">
          <h2 className="text-mydarkblue dark:text-myyellow-1 text-3xl font-limelight border-b w-fit">
            My lists &gt; {listName}
          </h2>
          <SearchBar value={searchTerm} onChange={setSearchTerm} />
        </div>

        {loading && (
          <p className="text-mydarkblue dark:text-myyellow-1">
            Loading movies...
          </p>
        )}

        {error && <ErrorAlert status={error.status} message={error.message} />}

        <div className="flex flex-wrap gap-6 text-mydarkblue dark:text-mylightgrey font-serif text-2xl text-wrap">
          {filteredMovies.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>

        {!filteredMovies.length && !loading && (
          <p className="my-20 font-bold text-2xl dark:text-mylightgrey">
            No movies found.
          </p>
        )}
      </div>

      <ShareListButton list={list} />
      <DeleteListButton listID={listID} />
    </>
  );
}

export default List;
