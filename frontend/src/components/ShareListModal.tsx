import axios from "axios";
import api from "../api";
import { useEffect, useState } from "react";

interface MovieList {
  id: number;
  name: string;
  slug: string;
  movies: number[];
  shared_with: number[];
}

interface Props {
  list: MovieList;
  onClose: () => void;
}

function ShareListModal(props: Props) {
  const [username, setUsername] = useState("");
  const [sharedWith, setSharedWith] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const users: string[] = [];

        for (const userID of props.list.shared_with) {
          const res = await api.get(`users/${userID}/`);
          users.push(res.data.username);
        }

        setSharedWith(users);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          setError(
            `ERROR ${err.response.status}: ${
              err.response.data?.error || "Unknown error"
            }`
          );
        } else {
          setError("Cannot get usernames");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (!username.trim()) return;

    api
      .post(`/lists/slug/${props.list.slug}/share/`, { username: username })
      .then(() => {
        const users = [...sharedWith];
        if (users.indexOf(username) === -1) {
          users.push(username);
          setSharedWith(users);
        }
      })
      .catch((err) => {
        if (axios.isAxiosError(err) && err.response) {
          setError(
            `ERROR ${err.response.status}: ${
              err.response.data?.error || "Unknown error"
            }`
          );
        } else {
          setError("Cannot share list");
        }
      });
  }

  const stopSharing = (username: string) => {
    api
      .delete(`/lists/slug/${props.list.slug}/share/`, {
        data: { username: username },
      })
      .then(() => {
        const idx = sharedWith.indexOf(username);
        const users = [...sharedWith];
        users.splice(idx, 1);
        setSharedWith(users);
      })
      .catch((err) => {
        if (axios.isAxiosError(err) && err.response) {
          setError(
            `ERROR ${err.response.status}: ${
              err.response.data?.error || "Unknown error"
            }`
          );
        } else {
          setError("Cannot remove from list");
        }
      });
  };

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
      <div className="bg-mylightgrey rounded-xl flex flex-col gap-6 w-[80%] max-w-2xl h-[80%] p-10 overflow-y-auto">
        <h1 className="border-b w-full text-4xl">Shared with</h1>
        {loading && <p className="text-mydarkblue">Loading users...</p>}
        <ul className="list-disc mx-10 text-3xl">
          {sharedWith.length === 0 && <p>Shared with nobody</p>}
          {sharedWith.map((username) => {
            return (
              <li className="my-5" key={username}>
                <span className="mr-5">{username}</span>
                <button
                  className="bg-red-400 text-black text-xl px-5 py-4 rounded-full font-limelight hover:cursor-pointer"
                  onClick={() => {
                    stopSharing(username);
                  }}
                >
                  Stop sharing
                </button>
              </li>
            );
          })}
        </ul>
        <form
          onSubmit={handleSubmit}
          className="bg-mylightgrey rounded-xl flex flex-col gap-6 max-w-2xl"
        >
          <h1 className="border-b w-full text-4xl">Share list</h1>

          <input
            className="bg-myyellow-1 text-mydarkblue font-bold text-2xl px-6 py-4 rounded-lg w-full"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <button
            type="submit"
            className="bg-mymint text-black text-3xl px-10 py-4 rounded-full font-limelight hover:cursor-pointer"
          >
            Share
          </button>
          {error && <p className="text-red-500">{error}</p>}
        </form>
      </div>
    </div>
  );
}

export default ShareListModal;
