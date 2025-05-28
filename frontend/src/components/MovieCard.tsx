import { useState } from "react";
import MovieModal from "./MovieModal";

interface Movie {
  id: number;
  title: string;
  description: string;
  poster_path: string;
  genres: number[];
}

interface Props {
  movie: Movie;
}

function MovieCard({ movie }: Props) {
  const imageUrl = `url(https://image.tmdb.org/t/p/original${movie.poster_path})`;

  const [isOpen, setIsOpen] = useState(false);

  function handleClick() {
    setIsOpen(true);
  }

  function handleClose() {
    setIsOpen(false);
  }

  return (
    <>
      <div className="w-48 h-60 my-10 cursor-pointer" onClick={handleClick}>
        <div
          style={{
            backgroundImage: imageUrl,
          }}
          className="w-48 h-60 rounded-xl flex items-center justify-center text-myturquoise font-pacifico text-xl hover:shadow-lg  transition-transform hover:scale-105 bg-cover bg-no-repeat bg-center"
        ></div>
        <p>{movie.title}</p>
      </div>
      {isOpen && <MovieModal movie={movie} onClose={handleClose} />}
    </>
  );
}

export default MovieCard;
