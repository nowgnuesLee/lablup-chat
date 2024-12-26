import { useCallback, useEffect, useState } from "react";
import ChatContainer from "./_components/ChatContainer";
import Header from "./_components/Header";
import InputContainer from "./_components/InputContainer";
import { message, ChattingContext } from "./hooks/useMessageList";
import useWS from "./hooks/useWS";

const Chat = () => {
  // state
  const [messageList, setMessageList] = useState<message[]>([]);
  // hooks
  const ws = useWS();

  const addMessage = useCallback(
    (msg: message) => {
      setMessageList((prev) => [...prev, msg]);
    },
    [setMessageList]
  );
  // useEffect
  useEffect(() => {
    if (!ws) return;
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      addMessage(msg);
    };
  }, [ws]);
  return (
    <ChattingContext.Provider
      value={{
        messageList,
        addMessage,
        userId: "1",
        ws,
      }}
    >
      <div className="relative flex flex-col w-full h-full overflow-y-scroll bg-primary-main">
        <Header />
        <ChatContainer />
        <InputContainer />
      </div>
    </ChattingContext.Provider>
  );
};

export default Chat;
