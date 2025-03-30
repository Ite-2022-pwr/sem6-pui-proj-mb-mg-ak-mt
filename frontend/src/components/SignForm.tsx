import { FormEvent, useState } from "react";

interface Props {
  route: "/login" | "/register";
  heading: "Login" | "Register";
}

function SignForm({ route, heading }: Props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [email, setEmail] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();

    if (
      !username.trim() ||
      !password.trim() ||
      !email.trim() ||
      !confirmPassword.trim()
    )
      return;

    if (password !== confirmPassword) return;

    alert(route + "\nUsername: " + username + "\nPassword: " + password);
  };

  return (
    <>
      <div className=" max-w-lg mx-auto bg-slate-100 rounded-md p-5 space-y-6">
        <h1 className="font-bold text-3xl text-center">{heading}</h1>
        <form className="flex flex-col space-y-5" onSubmit={handleSubmit}>
          <input
            value={username}
            name="username"
            onChange={(event) => setUsername(event.target.value)}
            placeholder="Username"
            className="rounded-s-md grow border border-gray-400 p-2 bg-white"
          />

          {route === "/register" && (
            <input
              value={email}
              name="email"
              onChange={(event) => setEmail(event.target.value)}
              placeholder="E-mail address"
              className="rounded-s-md grow border border-gray-400 p-2 bg-white"
            />
          )}

          <input
            value={password}
            name="password"
            type="password"
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Password"
            className="rounded-s-md grow border border-gray-400 p-2 bg-white"
          />

          {route === "/register" && (
            <input
              value={confirmPassword}
              type="password"
              onChange={(event) => setConfirmPassword(event.target.value)}
              placeholder="Confirm password"
              className="rounded-s-md grow border border-gray-400 p-2 bg-white"
            />
          )}

          {password == confirmPassword ? (
            <button
              type="submit"
              className="w-32 h-10 m-auto text-center space-x-10 justify-center rounded-md bg-slate-900 text-white hover:bg-slate-700"
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
