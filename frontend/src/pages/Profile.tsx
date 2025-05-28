import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import Navbar from "../components/Navbar";

function Profile() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const navigate = useNavigate();

  const getUserInfo = async () => {
    try {
      const response = await api.get("/users/me");
      setUsername(response.data.username);
      setEmail(response.data.email);
    } catch (error) {
      alert(error);
    }
  };

  const handleLogout = async () => {
    api.post("/auth/logout");
    localStorage.clear();
    navigate("/login");
  };

  if (username === "" || email === "") {
    getUserInfo();
  }

  return (
    <>
      <Navbar />

      <div className="font-semibold text-2xl my-10 mx-20 p-10">
        <ul className="flex flex-col gap-10">
          <li>
            Username:{" "}
            <span className="mx-5 font-mono font-normal">{username}</span>
          </li>
          <li>
            E-mail address:{" "}
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
    </>
  );
}

export default Profile;
