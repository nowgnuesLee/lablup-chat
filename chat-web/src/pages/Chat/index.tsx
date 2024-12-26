import { useCallback, useState } from "react";
import ChatContainer from "./_components/ChatContainer";
import Header from "./_components/Header";
import InputContainer from "./_components/InputContainer";
import { message, MessageListContext } from "./hooks/useMessageList";

const Chat = () => {
  const [messageList, setMessageList] = useState<message[]>([]);

  const addMessage = useCallback(
    (msg: message) => {
      setMessageList((prev) => [...prev, msg]);
    },
    [setMessageList]
  );
  return (
    <MessageListContext.Provider
      value={{
        messageList,
        addMessage,
        userId: "1",
      }}
    >
      <div className="relative flex flex-col w-full h-full overflow-y-scroll bg-primary-main">
        <Header />
        <ChatContainer />
        <InputContainer />
      </div>
    </MessageListContext.Provider>
  );
};

export default Chat;
