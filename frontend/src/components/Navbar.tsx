import { useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";
import { FaUser, FaBars, FaTimes } from "react-icons/fa";
import ThemeSwitch from "./ThemeSwitch";

function Navbar() {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => setMenuOpen((prev) => !prev);
  const closeMenu = () => setMenuOpen(false);

  return (
    <div className="bg-mydarkblue text-myyellow-1 sticky top-0 z-50">
      <div className="flex items-center justify-between px-4 py-3 md:px-8">
        <img
          src={logo}
          className="h-auto w-auto max-h-20 cursor-pointer"
          onClick={() => {
            navigate("/");
            closeMenu();
          }}
        />

        <button
          className="md:hidden text-2xl"
          onClick={toggleMenu}
          aria-label="Toggle menu"
        >
          {menuOpen ? <FaTimes /> : <FaBars />}
        </button>

        <ul className="hidden md:flex flex-row items-center gap-7 font-limelight text-2xl">
          <li
            className="hover:underline cursor-pointer"
            onClick={() => navigate("/browse")}
          >
            Browse movies
          </li>
          <li
            className="hover:underline cursor-pointer"
            onClick={() => navigate("/")}
          >
            My lists
          </li>
          <li>
            <ThemeSwitch />
          </li>
          <li>
            <button
              className="bg-myyellow-1 rounded-full w-10 h-10 flex items-center justify-center hover:cursor-pointer hover:bg-myyellow-2"
              onClick={() => navigate("/profile")}
            >
              <FaUser className="text-mydarkblue text-lg" />
            </button>
          </li>
        </ul>
      </div>

      {menuOpen && (
        <ul className="flex flex-col gap-4 px-4 pb-4 md:hidden font-limelight text-2xl bg-mydarkblue border-t border-myyellow-1 pt-5">
          <li
            className="hover:underline cursor-pointer"
            onClick={() => {
              navigate("/browse");
              closeMenu();
            }}
          >
            Browse movies
          </li>
          <li
            className="hover:underline cursor-pointer"
            onClick={() => {
              navigate("/");
              closeMenu();
            }}
          >
            My lists
          </li>
          <li>
            <ThemeSwitch />
          </li>
          <li>
            <button
              className="bg-myyellow-1 rounded-full w-10 h-10 flex items-center justify-center hover:cursor-pointer hover:bg-myyellow-2"
              onClick={() => {
                navigate("/profile");
                closeMenu();
              }}
            >
              <FaUser className="text-mydarkblue text-lg" />
            </button>
          </li>
        </ul>
      )}
    </div>
  );
}

export default Navbar;
