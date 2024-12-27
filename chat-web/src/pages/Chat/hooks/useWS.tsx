import { useEffect, useState } from "react";

const useWS = () => {
  const [ws, setWS] = useState<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8080/chat");

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
