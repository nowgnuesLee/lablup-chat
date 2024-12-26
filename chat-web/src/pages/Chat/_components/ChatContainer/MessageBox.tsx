interface MessageBoxProps {
  message: string;
  user: string;
  isSender: boolean;
}

const MessageBox = ({ message, user, isSender }: MessageBoxProps) => {
  const getAlign = () => {
    if (isSender) {
      return "items-end";
    } else {
      return "items-start";
    }
  };
  const getBgColor = () => {
    if (isSender) {
      return "bg-primary-sub";
    } else {
      return "bg-white";
    }
  };
  return (
    <div className={`flex flex-col w-full gap-1 ${getAlign()} px-4`}>
      <p className="text-neutral-300">{user}</p>
      <pre className={`px-4 py-2 text-black rounded-2xl ${getBgColor()}`}>
        {message}
      </pre>
    </div>
  );
};

export default MessageBox;
