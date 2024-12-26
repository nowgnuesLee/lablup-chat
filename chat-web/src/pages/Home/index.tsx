import { useNavigate } from "react-router";

const Home = () => {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col items-center justify-center w-full h-full">
      <h1 className="mb-8 text-2xl font-bold">
        Click the button and start a new chat!
      </h1>
      <button
        type="button"
        className="px-4 py-2 font-bold text-white bg-blue-500 rounded  hover:bg-blue-700"
        onClick={() => navigate("/chat")}
      >
        Start Chat
      </button>
    </div>
  );
};

export default Home;
