import { useMessageList } from "../../hooks/useMessageList";
import MessageBox from "./MessageBox";

const ChatContainer = () => {
  // hooks
  const { messageList, userId } = useMessageList();

  return (
    <section className="flex flex-col flex-1 w-full gap-4 py-4 text-white">
      {messageList.map((msg, index) => (
        <MessageBox
          key={`msg-${msg.userId}-${index}`}
          message={msg.message}
          user={msg.userId}
          isSender={msg.userId === userId}
        />
      ))}
    </section>
  );
};

export default ChatContainer;
