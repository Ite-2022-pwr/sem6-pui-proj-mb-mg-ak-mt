import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import Navbar from "../components/Navbar";

interface User {
  username: string;
  email: string;
}

function Profile() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const getUserInfo = async () => {
      try {
        const response = await api.get<User>("/users/me");

        setUsername(response.data.username);
        setEmail(response.data.email);
      } catch (error) {
        alert(error);
      }
    };

    getUserInfo();
  }, []);

  const handleLogout = async () => {
    api.post("/auth/logout");
    localStorage.clear();
    navigate("/login");
  };

  return (
    <>
      <Navbar />

      <div className="bg-mylightgrey dark:bg-mydarkgrey min-h-screen px-8 py-4">
        <div className="font-semibold text-2xl my-10 mx-20 p-10 bg-mylightgrey dark:bg-mydarkgrey">
          <ul className="flex flex-col gap-10 dark:text-mylightgrey">
            <li>
              Username:
              <span className="mx-5 font-mono font-normal">{username}</span>
            </li>
            <li>
              E-mail address:
              <span className="mx-5 font-mono font-normal">{email}</span>
            </li>
          </ul>
          <button
            className="bg-myyellow-2 p-5 font-limelight my-10 hover:bg-myyellow-1 hover:cursor-pointer rounded-2xl"
            onClick={() => {
              handleLogout();
            }}
          >
            Logout
          </button>
        </div>
      </div>
    </>
  );
}

export default Profile;
