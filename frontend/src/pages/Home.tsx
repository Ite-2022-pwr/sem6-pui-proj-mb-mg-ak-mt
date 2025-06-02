import axios from "axios";
import api from "../api";
import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import ListCard from "../components/ListCard";
import NewListButton from "../components/NewListButton";

interface MovieList {
  id: number;
  name: string;
  slug: string;
}

function Home() {
  const [lists, setLists] = useState<MovieList[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLists = async () => {
      try {
        const response = await api.get<MovieList[]>("/lists/me");
        setLists(response.data);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          setError(
            `ERROR ${err.response.status}: ${
              err.response.data?.error || "Unknown error"
            }`
          );
        } else {
          setError("Cannot load lists");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchLists();
  }, []);

  return (
    <>
      <Navbar />
      <div className="bg-mylightgrey dark:bg-mydarkgrey min-h-screen px-8 py-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-mydarkblue dark:text-myyellow-1 text-3xl font-limelight border-b w-fit">
            My lists
          </h2>
          <input
            type="text"
            placeholder="Search"
            className="rounded-full px-4 py-1 bg-myyellow-1 text-mydarkblue placeholder-mydarkblue focus:outline-none w-48"
          />
        </div>

        {loading && (
          <p className="text-mydarkblue dark:text-myyellow-1">
            Loading lists...
          </p>
        )}
        {error && <p className="text-red-500">{error}</p>}

        <div className="flex flex-wrap gap-6 text-mymint font-limelight">
          {lists.map(function (list) {
            return <ListCard key={list.id} name={list.name} slug={list.slug} />;
          })}
        </div>

        <NewListButton />
      </div>
    </>
  );
}

export default Home;
