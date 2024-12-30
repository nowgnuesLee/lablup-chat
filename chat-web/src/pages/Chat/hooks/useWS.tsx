import { useEffect, useState } from "react";

const SERVER_HOST = import.meta.env.VITE_SERVER_HOST;
const SERVER_PORT = import.meta.env.VITE_SERVER_PORT;

const useWS = () => {
  const [ws, setWS] = useState<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(`ws://${SERVER_HOST}:${SERVER_PORT}/chat`);

    ws.onopen = () => {
      console.log("connected");
    };

    setWS(ws);

    return () => {
      ws.close();
    };
  }, []);

  return ws;
};

export default useWS;
