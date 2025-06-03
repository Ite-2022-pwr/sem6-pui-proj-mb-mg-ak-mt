import axios from "axios";
import api from "../api";
import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import MovieCard from "../components/MovieCard";
import DeleteListButton from "../components/DeleteListButton";
import ShareListButton from "../components/ShareListButton";
import SearchBar from "../components/SearchBar";

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
  const [listName, setListName] = useState<string | null>("");
  const [movies, setMovies] = useState<Movie[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [listID, setListID] = useState<number>(-1);
  const [list, setList] = useState<MovieList>({
    id: -1,
    name: "",
    slug: "",
    movies: [],
    shared_with: [],
  });
  const [searchTerm, setSearchTerm] = useState<string>("");

  useEffect(() => {
    const listSlug = new URLSearchParams(window.location.search).get("slug");

    const fetchMovies = async () => {
      try {
        const responseList = await api.get<MovieList>(
          `/lists/slug/${listSlug}`
        );

        setListID(responseList.data.id);
        setListName(responseList.data.name);
        setList(responseList.data);

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
              err.response.data?.error || "Unknown error"
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
        {error && <p className="text-red-500">{error}</p>}

        <div className="flex flex-wrap gap-6 text-mydarkblue dark:text-mylightgrey font-serif text-2xl text-wrap">
          {filteredMovies.map((movie) => {
            return <MovieCard key={movie.id} movie={movie} />;
          })}
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
