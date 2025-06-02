import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";
import { FaUser } from "react-icons/fa";
import ThemeSwitch from "./ThemeSwitch";

function Navbar() {
  const navigate = useNavigate();

  return (
    <div className="bg-mydarkblue text-myyellow-1 flex flex-row items-center justify-between top-0 sticky">
      <img src={logo} className="flex" />
      <ul className="flex flex-row font-limelight text-2xl gap-7 mx-5 items-center">
        <li
          className="w-24 leading-tight block text-center break-words hover:underline hover:cursor-pointer"
          onClick={() => {
            navigate("/browse");
          }}
        >
          Browse movies
        </li>
        <li
          className="block leading-tight hover:underline hover:cursor-pointer"
          onClick={() => {
            navigate("/");
          }}
        >
          My lists
        </li>

        <li>
          <ThemeSwitch />
        </li>

        <li>
          <button
            className="bg-myyellow-1 rounded-full w-12 h-12 flex items-center justify-center hover:cursor-pointer"
            onClick={() => {
              navigate("/profile");
            }}
          >
            <FaUser className="text-mydarkblue text-xl " />
          </button>
        </li>
      </ul>
    </div>
  );
}

export default Navbar;
