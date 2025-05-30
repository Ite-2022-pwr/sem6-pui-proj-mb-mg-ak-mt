import { useNavigate } from "react-router-dom";
import api from "../api";
import { FaTrash } from "react-icons/fa";

interface Props {
  listID: number;
}

function DeleteListButton({ listID }: Props) {
  const navigate = useNavigate();

  const handleClick = () => {
    api
      .delete(`/lists/${listID}/`)
      .then(() => {
        alert("List deleted");
        navigate("/");
      })
      .catch((err) => {
        alert(err);
      });
  };

  return (
    <button
      onClick={handleClick}
      className="fixed bottom-6 right-6 bg-myyellow-1 text-mydarkblue rounded-full w-16 h-16 text-3xl flex items-center justify-center shadow-md hover:scale-105 transition-transform hover:cursor-pointer hover:bg-myyellow-2"
    >
      <FaTrash />
    </button>
  );
}

export default DeleteListButton;
