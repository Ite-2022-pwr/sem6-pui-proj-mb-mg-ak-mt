import { useState } from "react";
import NewListModal from "./NewListModal";
import { FaPlus } from "react-icons/fa";

function NewListButton() {
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
        className="fixed bottom-6 right-6 bg-myyellow-1 text-mydarkblue rounded-full w-16 h-16 text-4xl flex items-center justify-center shadow-md hover:scale-105 transition-transform hover:cursor-pointer hover:bg-myyellow-2"
      >
        <FaPlus />
      </button>
      {isOpen && (
        <NewListModal
          onCreated={() => {
            window.location.reload();
          }}
          onClose={handleClose}
        />
      )}
    </>
  );
}

export default NewListButton;
