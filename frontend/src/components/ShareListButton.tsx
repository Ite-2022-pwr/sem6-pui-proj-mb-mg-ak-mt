import { useState } from "react";
import { FaShare } from "react-icons/fa";
import ShareListModal from "./ShareListModal";

interface MovieList {
  id: number;
  name: string;
  slug: string;
  movies: number[];
  shared_with: number[];
}

interface Props {
  list: MovieList;
}

function ShareListButton({ list }: Props) {
  const [isOpen, setIsOpen] = useState(false);

  function handleClick() {
    setIsOpen(true);
  }

  function handleClose() {
    setIsOpen(false);
  }

  return (
    <>
      <button
        onClick={handleClick}
        className="fixed bottom-28 right-6 bg-myyellow-1 text-mydarkblue rounded-full w-16 h-16 text-3xl flex items-center justify-center shadow-md hover:scale-105 transition-transform hover:cursor-pointer hover:bg-myyellow-2"
      >
        <FaShare />
      </button>

      {isOpen && <ShareListModal list={list} onClose={handleClose} />}
    </>
  );
}

export default ShareListButton;
