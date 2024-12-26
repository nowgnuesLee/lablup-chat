import { useMessageList } from "../../hooks/useMessageList";
import MessageBox from "./MessageBox";

const ChatContainer = () => {
  // hooks
  const { messageList, userId } = useMessageList();
  console.log(messageList, userId);
  return (
    <section className="flex flex-col flex-1 w-full gap-4 py-4 text-white">
      {messageList.map((msg, index) => (
        <MessageBox
          key={`msg-${msg.id}-${index}`}
          message={msg.context}
          user={msg.id}
          isSender={msg.id === userId}
        />
      ))}
    </section>
  );
};

export default ChatContainer;
