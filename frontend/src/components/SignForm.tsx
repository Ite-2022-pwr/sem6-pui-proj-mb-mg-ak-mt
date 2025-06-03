import { FormEvent, useState } from "react";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";

interface Props {
  route: "/login" | "/register";
  heading: "Login" | "Register";
  onError?: (err: { status?: number; message: string }) => void;
}

function SignForm({ route, heading, onError }: Props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [email, setEmail] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    if (!username.trim() || !password.trim()) {
      onError?.({ message: "Username and password are required." });
      return;
    }

    if (route === "/register") {
      if (!email.trim() || !confirmPassword.trim()) {
        onError?.({ message: "Email and confirm password are required." });
        return;
      }

      if (password !== confirmPassword) {
        onError?.({ message: "Passwords don't match." });
        return;
      }
    }

    try {
      if (route === "/login") {
        const response = await api.post("/auth" + route + "/", {
          username: username,
          password: password,
        });
        localStorage.setItem(ACCESS_TOKEN, response.data.token);
        navigate("/");
      } else {
        const response = await api.post("/auth" + route + "/", {
          username: username,
          password: password,
          email: email,
        });
        alert(`Created user ${response.data.username}`);
        navigate("/login");
      }
    } catch (error: any) {
      if (error.response) {
        onError?.({
          status: error.response.status,
          message: error.response.data?.message || "An error occurred.",
        });
      } else {
        onError?.({ message: "Network error. Please try again." });
      }
    }
  };

  return (
    <>
      <img src={logo} className="flex mx-auto" alt="Logo" />
      <div className=" max-w-lg mx-auto bg-mylightgrey rounded-md p-5 space-y-6">
        <form className="flex flex-col space-y-5" onSubmit={handleSubmit}>
          <input
            value={username}
            name="username"
            onChange={(event) => setUsername(event.target.value)}
            placeholder="Username"
            className="rounded-s-md grow p-2 bg-myyellow-1 my-5"
          />

          {route === "/register" && (
            <input
              value={email}
              name="email"
              onChange={(event) => setEmail(event.target.value)}
              placeholder="E-mail address"
              className="rounded-s-md grow p-2 bg-myyellow-1 my-5"
            />
          )}

          <input
            value={password}
            name="password"
            type="password"
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Password"
            className="rounded-s-md grow p-2 bg-myyellow-1 my-5"
          />

          {route === "/register" && (
            <input
              value={confirmPassword}
              type="password"
              onChange={(event) => setConfirmPassword(event.target.value)}
              placeholder="Confirm password"
              className="rounded-s-md grow p-2 bg-myyellow-1 my-5"
            />
          )}

          {route === "/login" || password === confirmPassword ? (
            <button
              type="submit"
              className="flex items-center p-7 w-32 h-10 m-auto space-x-10 justify-center rounded-lg bg-myyellow-2 text-black text-2xl font-limelight hover:bg-myyellow-1 hover:cursor-pointer my-5"
            >
              {heading}
            </button>
          ) : (
            <p className="text-red-500 m-auto font-bold text-xl">
              Passwords don't match
            </p>
          )}
        </form>
      </div>
    </>
  );
}

export default SignForm;
