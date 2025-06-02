import { useEffect, useState } from "react";

function ThemeSwitch() {
  const [isChecked, setIsChecked] = useState<boolean>(false);

  useEffect(() => {
    if (isChecked) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isChecked]);

  const onChange = () => {
    setIsChecked(!isChecked);
  };

  return (
    <label className="relative inline-flex items-center cursor-pointer">
      <input
        type="checkbox"
        className="sr-only peer"
        checked={isChecked}
        onChange={onChange}
      />
      <div className="w-14 h-8 bg-myyellow-1 rounded-full peer-checked:bg-myyellow-1 relative transition-all duration-300 peer-checked:[&>div]:translate-x-6">
        <div className="absolute left-1 top-1 bg-mydarkgrey w-6 h-6 rounded-full transition-all duration-300 "></div>
      </div>
    </label>
  );
}

export default ThemeSwitch;
