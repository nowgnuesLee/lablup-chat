import { useNavigate } from "react-router";

const Header = () => {
  const nav = useNavigate();
  return (
    <header className="sticky top-0 left-0 z-50 flex items-center justify-between w-full px-4 py-4 text-white bg-primary-main">
      <button
        className="text-3xl text-center"
        type="button"
        onClick={() => nav("/")}
      >
        {"<"}
      </button>
      <h1 className="text-2xl font-bold">Lablup</h1>
      <button
        disabled
        className="text-3xl text-center text-transparent"
        type="button"
      >
        {"<"}
      </button>
    </header>
  );
};

export default Header;
