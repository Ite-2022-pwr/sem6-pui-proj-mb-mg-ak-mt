import logo from "../assets/logo.png";
import { FaUser } from "react-icons/fa";

function Navbar() {
  return (
    <div className="bg-mydarkblue text-myyellow-1 flex flex-row items-center justify-between">
      <img src={logo} className="flex" />
      <ul className="flex flex-row font-limelight text-2xl gap-7 mx-5 items-center">
        <li className="w-24 leading-tight block text-center break-words hover:underline hover:cursor-pointer">
          Browse movies
        </li>
        <li className="block leading-tight hover:underline hover:cursor-pointer">
          My lists
        </li>

        <li>
          <label className="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" className="sr-only peer" />
            <div className="w-14 h-8 bg-myyellow-1 rounded-full peer-checked:bg-myyellow-1 relative transition-all duration-300 peer-checked:[&>div]:translate-x-6">
              <div className="absolute left-1 top-1 bg-mydarkgrey w-6 h-6 rounded-full transition-all duration-300 "></div>
            </div>
          </label>
        </li>

        <li>
          <button className="bg-myyellow-1 rounded-full w-12 h-12 flex items-center justify-center">
            <FaUser className="text-mydarkblue text-xl hover:cursor-pointer" />
          </button>
        </li>
      </ul>
    </div>
  );
}

export default Navbar;
