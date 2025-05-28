import { useNavigate } from "react-router-dom";

interface Props {
  name: string;
  slug: string;
}

function ListCard({ name, slug }: Props) {
  const navigate = useNavigate();

  return (
    <div
      className="bg-mydarkblue w-48 h-60 rounded-xl flex items-center justify-center text-myturquoise font-pacifico text-xl hover:shadow-lg cursor-pointer transition-transform hover:scale-105"
      onClick={() => navigate(`/list?slug=${slug}`)}
    >
      {name}
    </div>
  );
}

export default ListCard;
