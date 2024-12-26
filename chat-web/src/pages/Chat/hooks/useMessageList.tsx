import { createContext, useContext } from "react";

export type message = {
  id: string;
  context: string;
};

export type messageListContext = {
  messageList: message[];
  addMessage: (message: message) => void;
  userId: string;
};

export const MessageListContext = createContext<messageListContext | undefined>(
  undefined
);

export const useMessageList = () => {
  const context = useContext(MessageListContext);
  if (!context) {
    throw new Error("useMessageList must be used within MessageListProvider");
  }
  return context;
};
