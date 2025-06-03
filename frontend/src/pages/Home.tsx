import axios from "axios";
import { useEffect, useState } from "react";
import api from "../api";
import Navbar from "../components/Navbar";
import ListCard from "../components/ListCard";
import NewListButton from "../components/NewListButton";
import SearchBar from "../components/SearchBar";
import ErrorAlert from "../components/ErrorAlert";

interface MovieList {
  id: number;
  name: string;
  slug: string;
}

function Home() {
  const [lists, setLists] = useState<MovieList[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<{
    status?: number;
    message: string;
  } | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");

  useEffect(() => {
    const fetchLists = async () => {
      try {
        const response = await api.get<MovieList[]>("/lists/me");
        setLists(response.data);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
          setError({
            status: err.response.status,
            message: err.response.data?.error || "Unknown error",
          });
        } else {
          setError({ message: "Cannot load lists" });
        }
      } finally {
        setLoading(false);
      }
    };

    fetchLists();
  }, []);

  const filteredLists = lists.filter((list) =>
    list.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Navbar />
      <div className="bg-mylightgrey dark:bg-mydarkgrey min-h-screen px-8 py-4">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 gap-2">
          <h2 className="text-mydarkblue dark:text-myyellow-1 text-3xl font-limelight border-b w-fit">
            My lists
          </h2>
          <SearchBar value={searchTerm} onChange={setSearchTerm} />
        </div>

        {loading && (
          <p className="text-mydarkblue dark:text-myyellow-1">
            Loading lists...
          </p>
        )}

        {error && <ErrorAlert status={error.status} message={error.message} />}

        <div className="flex flex-wrap gap-6 text-mymint font-limelight">
          {filteredLists.length > 0
            ? filteredLists.map((list) => (
                <ListCard key={list.id} name={list.name} slug={list.slug} />
              ))
            : !loading && (
                <p className="text-mydarkblue dark:text-myyellow-1">
                  No lists found.
                </p>
              )}
        </div>

        <NewListButton />
      </div>
    </>
  );
}

export default Home;
