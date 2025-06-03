import axios from "axios";
import { useState, useEffect } from "react";
import api from "../api";
import Navbar from "../components/Navbar";
import MovieCard from "../components/MovieCard";
import SearchBar from "../components/SearchBar";

interface Movie {
  id: number;
  title: string;
  description: string;
  poster_path: string;
  genres: number[];
}

function BrowseMovies() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await api.get<Movie[]>("/movies");
        setMovies(response.data);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          setError(
            `ERROR ${err.response.status}: ${
              err.response.data?.browse || "Unknown error"
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

  const filteredMovies = movies.filter((movie) =>
    movie.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

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

        {loading && (
          <p className="text-mydarkblue dark:text-myyellow-1">
            Loading movies...
          </p>
        )}
        {error && <p className="text-red-500">{error}</p>}

        <div className="flex flex-wrap justify-center md:justify-start gap-6 text-mydarkblue dark:text-mylightgrey font-serif text-2xl">
          {filteredMovies.length > 0 ? (
            filteredMovies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))
          ) : (
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
