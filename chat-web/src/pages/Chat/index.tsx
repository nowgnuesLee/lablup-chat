import { useCallback, useEffect, useState } from "react";
import ChatContainer from "./_components/ChatContainer";
import Header from "./_components/Header";
import InputContainer from "./_components/InputContainer";
import { message, ChattingContext } from "./hooks/useMessageList";
import useWS from "./hooks/useWS";

const Chat = () => {
  // state
  const [messageList, setMessageList] = useState<message[]>([]);
  const [userId, setUserId] = useState<string | null>(null);
  console.log(userId);
  // hooks
  const ws = useWS();

  const addMessage = useCallback(
    (msg: message) => {
      if (msg.userId !== userId) {
        setMessageList((prev) => [...prev, msg]);
      }
    },
    [setMessageList, userId]
  );
  // useEffect
  useEffect(() => {
    if (!ws) return;
    ws.onmessage = (event) => {
      const msg: message = JSON.parse(event.data);
      console.log(msg);
      if (msg.type === "info") {
        console.log(msg.userId);
        setUserId(msg.userId);
      } else if (msg.type === "message") {
        console.log({
          userId,
          msgUser: msg.userId,
        });
        addMessage(msg);
      }
    };
  }, [ws]);

  if (!ws || !userId) {
    console.log(ws, userId);
    return (
      <div className="flex items-center justify-center w-full h-full">
        Connecting...
      </div>
    );
  }

  return (
    <ChattingContext.Provider
      value={{
        messageList,
        addMessage,
        userId,
        ws,
      }}
    >
      <div className="relative flex flex-col w-full h-full overflow-y-scroll bg-primary-main scrollbar-hide">
        <Header />
        <ChatContainer />
        <InputContainer />
      </div>
    </ChattingContext.Provider>
  );
};

export default Chat;
