import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import Navbar from "../components/Navbar";
import ErrorAlert from "../components/ErrorAlert";

interface User {
  username: string;
  email: string;
}

function Profile() {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<{
    message: string;
    status?: number;
  } | null>(null);

  const navigate = useNavigate();

  useEffect(() => {
    const getUserInfo = async () => {
      try {
        const response = await api.get<User>("/users/me");
        setUser(response.data);
      } catch (err: any) {
        if (err.response) {
          setError({
            status: err.response.status,
            message: err.response.data?.error || "Failed to load user info",
          });
        } else {
          setError({ message: "Network error or server not responding." });
        }
      }
    };

    getUserInfo();
  }, []);

  const handleLogout = async () => {
    try {
      await api.post("/auth/logout");
    } catch {
      // Optional: handle logout error
    } finally {
      localStorage.clear();
      navigate("/login");
    }
  };

  return (
    <>
      <Navbar />

      <div className="bg-mylightgrey dark:bg-mydarkgrey min-h-screen px-8 py-4">
        <div className="font-semibold text-2xl my-10 mx-20 p-10 bg-mylightgrey dark:bg-mydarkgrey">
          {error && (
            <ErrorAlert status={error.status} message={error.message} />
          )}

          {user ? (
            <>
              <ul className="flex flex-col gap-10 dark:text-mylightgrey">
                <li>
                  Username:
                  <span className="mx-5 font-mono font-normal">
                    {user.username}
                  </span>
                </li>
                <li>
                  E-mail address:
                  <span className="mx-5 font-mono font-normal">
                    {user.email}
                  </span>
                </li>
              </ul>

              <button
                className="bg-myyellow-2 p-5 font-limelight my-10 hover:bg-myyellow-1 hover:cursor-pointer rounded-2xl"
                onClick={handleLogout}
              >
                Logout
              </button>
            </>
          ) : (
            !error && (
              <p className="text-mydarkblue dark:text-myyellow-1">
                Loading user info...
              </p>
            )
          )}
        </div>
      </div>
    </>
  );
}

export default Profile;
