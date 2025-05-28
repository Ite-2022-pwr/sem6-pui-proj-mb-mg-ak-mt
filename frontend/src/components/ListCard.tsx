interface Props {
  name: string;
}

function ListCard({ name }: Props) {
  return (
    <div className="bg-mydarkblue w-48 h-60 rounded-xl flex items-center justify-center text-myturquoise font-pacifico text-xl hover:shadow-lg cursor-pointer transition-transform hover:scale-105">
      {name}
    </div>
  );
}

export default ListCard;
