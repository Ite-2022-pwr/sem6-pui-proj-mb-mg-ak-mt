interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

function SearchBar({
  value,
  onChange,
  placeholder = "Search",
}: SearchBarProps) {
  return (
    <input
      type="text"
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="rounded-full px-4 py-1 bg-myyellow-1 text-mydarkblue placeholder-mydarkblue focus:outline-none w-full max-w-xs md:w-48"
    />
  );
}

export default SearchBar;
