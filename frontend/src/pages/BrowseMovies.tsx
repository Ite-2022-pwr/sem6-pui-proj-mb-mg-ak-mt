import axios from "axios";
import { useState, useEffect } from "react";
import api from "../api";
import Navbar from "../components/Navbar";
import MovieCard from "../components/MovieCard";

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

  return (
    <>
      <Navbar />
      <div className="bg-mylightgrey dark:bg-mydarkgrey min-h-screen px-8 py-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-mydarkblue dark:text-myyellow-1 text-3xl font-limelight border-b w-fit">
            Browse movies
          </h2>
          <input
            type="text"
            placeholder="Search"
            className="rounded-full px-4 py-1 bg-myyellow-1 text-mydarkblue placeholder-mydarkblue focus:outline-none w-48"
          />
        </div>

        {loading && (
          <p className="text-mydarkblue dark:text-myyellow-1">
            Loading movies...
          </p>
        )}
        {error && <p className="text-red-500">{error}</p>}

        <div className="flex flex-wrap gap-6 text-mydarkblue dark:text-mylightgrey font-serif text-2xl text-wrap">
          {movies.map((movie) => {
            return <MovieCard key={movie.id} movie={movie} />;
          })}
        </div>
      </div>
    </>
  );
}

export default BrowseMovies;
