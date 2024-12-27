import { useState } from "react";
import { useMessageList } from "../../hooks/useMessageList";

const InputContainer = () => {
  // state
  const [msg, setMsg] = useState("");
  // hooks
  const { addMessage, ws, userId } = useMessageList();
  // handler
  const handleSendMsg = () => {
    if (!ws) return;
    console.log(msg);
    const msgTrim = msg.trim();
    if (!msgTrim) return;
    ws.send(msgTrim);
    addMessage({
      type: "message",
      userId,
      message: msgTrim,
    });
    setMsg("");
  };
  const handleOnChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMsg(e.target.value);
  };
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMsg();
    }
  };
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleSendMsg();
  };
  return (
    <form
      className="sticky bottom-0 left-0 flex items-end w-full gap-2 px-3 py-2 bg-white"
      onSubmit={handleSubmit}
    >
      <textarea
        name="message"
        className="w-full h-24 p-1 text-black bg-[#F6F6F6] rounded-md outline-none border"
        placeholder={`${userId}, type a message...`}
        style={{
          resize: "none",
        }}
        onChange={handleOnChange}
        onKeyDown={handleKeyDown}
        value={msg}
      />
      <button
        type="submit"
        className="px-4 py-2 font-semibold text-black rounded-md bg-primary-sub hover:bg-[#ffe125]"
      >
        Send
      </button>
    </form>
  );
};

export default InputContainer;
