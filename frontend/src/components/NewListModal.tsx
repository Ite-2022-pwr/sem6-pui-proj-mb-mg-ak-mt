import axios from "axios";
import React, { useState } from "react";
import api from "../api";

interface Props {
  onClose: () => void;
  onCreated: () => void;
}

function NewListModal(props: Props) {
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!name.trim()) return;

    api
      .post("/lists/", { name: name, movies: [] })
      .then(() => {
        props.onCreated();
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
          setError("Cannot create list");
        }
      });
  }

  const closeModal = (event: React.MouseEvent) => {
    const modalBackground = document.getElementById("new-list-modal-bg");
    if (event.target === modalBackground) {
      props.onClose();
    }
  };

  return (
    <div
      id="new-list-modal-bg"
      className="fixed top-0 left-0 w-full h-full bg-black/75 flex items-center justify-center z-50"
      onClick={closeModal}
    >
      <form
        onSubmit={handleSubmit}
        className="bg-mylightgrey dark:bg-mydarkgrey p-10 rounded-xl flex flex-col items-center gap-6 w-[80%] max-w-2xl"
      >
        <input
          className="bg-myyellow-1 text-mydarkblue font-bold text-2xl px-6 py-4 rounded-lg w-full"
          placeholder="List name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button
          type="submit"
          className="bg-mymint text-black text-3xl px-10 py-4 rounded-full font-limelight hover:cursor-pointer hover:bg-green-400"
        >
          Create
        </button>
        {error && <p className="text-red-500">{error}</p>}
      </form>
    </div>
  );
}

export default NewListModal;
