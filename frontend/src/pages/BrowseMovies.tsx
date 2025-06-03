import axios from "axios";
import { useState, useEffect } from "react";
import api from "../api";
import Navbar from "../components/Navbar";
import MovieCard from "../components/MovieCard";
import SearchBar from "../components/SearchBar";
import ErrorAlert from "../components/ErrorAlert";

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

function BrowseMovies() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<{
    status?: number;
    message: string;
  } | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [selectedGenres, setSelectedGenres] = useState<number[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [moviesRes, genresRes] = await Promise.all([
          api.get<Movie[]>("/movies"),
          api.get<Genre[]>("/genres"),
        ]);

        setMovies(moviesRes.data);
        setGenres(genresRes.data);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          setError({
            status: err.response.status,
            message: err.response.data?.error || "Unknown error",
          });
        } else {
          setError({ message: "Cannot get movies or genres" });
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const toggleGenre = (genreId: number) => {
    setSelectedGenres((prev) =>
      prev.includes(genreId)
        ? prev.filter((id) => id !== genreId)
        : [...prev, genreId]
    );
  };

  const filteredMovies = movies.filter((movie) => {
    const search = searchTerm.toLowerCase();

    const matchesText =
      movie.title.toLowerCase().includes(search) ||
      movie.description.toLowerCase().includes(search);

    const matchesGenres =
      selectedGenres.length === 0 ||
      movie.genres.some((genreId) => selectedGenres.includes(genreId));

    return matchesText && matchesGenres;
  });

  return (
    <>
      <Navbar />

      <div className="bg-mylightgrey dark:bg-mydarkgrey min-h-screen px-4 sm:px-8 py-4">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 gap-2">
          <h2 className="text-mydarkblue dark:text-myyellow-1 text-3xl font-limelight border-b w-fit">
            Browse movies
          </h2>

          <SearchBar value={searchTerm} onChange={setSearchTerm} />
        </div>

        <div className="mb-4 flex flex-wrap gap-2">
          {genres.map((genre) => (
            <button
              key={genre.id}
              onClick={() => toggleGenre(genre.id)}
              className={`px-3 py-1 rounded-full border cursor-pointer select-none
        ${
          selectedGenres.includes(genre.id)
            ? "bg-myyellow-1 text-mydarkblue dark:bg-yellow-400 dark:text-gray-900 border-mydarkblue dark:border-myyellow-1"
            : "bg-transparent text-mydarkblue border-mydarkblue dark:text-myyellow-1 dark:border-myyellow-1"
        }
      `}
            >
              {genre.name}
            </button>
          ))}
        </div>

        {loading && (
          <p className="text-mydarkblue dark:text-myyellow-1">
            Loading movies...
          </p>
        )}

        {error && <ErrorAlert status={error.status} message={error.message} />}

        <div className="flex flex-wrap justify-center md:justify-start gap-6 text-mydarkblue dark:text-mylightgrey font-serif text-2xl">
          {filteredMovies.length > 0
            ? filteredMovies.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))
            : !loading && (
                <p className="text-center w-full text-mydarkblue dark:text-myyellow-1">
                  No movies found.
                </p>
              )}
        </div>
      </div>
    </>
  );
}

export default BrowseMovies;
