import { createContext, useContext } from "react";

export type message = {
  id: string;
  context: string;
};

export type chattingContext = {
  messageList: message[];
  addMessage: (message: message) => void;
  userId: string;
  ws: WebSocket | null;
};

export const ChattingContext = createContext<chattingContext | undefined>(
  undefined
);

export const useMessageList = () => {
  const context = useContext(ChattingContext);
  if (!context) {
    throw new Error("useMessageList must be used within MessageListProvider");
  }
  return context;
};
