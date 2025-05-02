import { memo, useEffect, useState } from "react";

interface message {
  data_type: "chat" | "system" | "time" | "clientinfo";
  data: {
    client_id?: number;
    message?: string;
    time?: string;
  };
}

function App() {
  const [chatMessages, setchatMessages] = useState<string[]>([]);
  const [systemMessages, setsystemMessages] = useState<string[]>([]);
  const [currentTime, setcurrentTime] = useState<string>("");
  const [totalclient, settotalclient] = useState<string>("")


  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [mysockid, setmysockid] = useState<Number | null>();
  const [inputMessage, setInputMessage] = useState("");

  function sockconnection() {
    const randomNumber = Math.floor(Math.random() * 1000);
    console.log("Generated random number:", randomNumber);
    setmysockid(randomNumber);

    try {
      const socket = new WebSocket(`ws://localhost:8000/ws/${randomNumber}`); // Make sure to include /ws path

      socket.onopen = () => {
        console.log("Connected to WebSocket server");
        setSocket(socket);
      };

      socket.onmessage = (event) => {
        try {
          const message: message = JSON.parse(event.data);

          switch (message.data_type) {
            case "chat":
              setchatMessages((prev) => [
                ...prev,
                `client #${message.data.client_id}: ${message.data.message}`,
              ]);
              break;

            case "system":
              setsystemMessages((prev) => [...prev, message.data.message!]);
              break;

            case "time":
              setcurrentTime(message.data.time!);
              break;

            case "clientinfo":
              settotalclient(message.data.message!)

          }
        } catch (error) {
          console.error("error parsing message:", error);
        }
      };

      socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        setSocket(null);
      };

      socket.onclose = () => {
        console.log("Disconnected from WebSocket server");
        // Optionally implement reconnection logic here
        setSocket(null);
      };

      return socket;
    } catch (error) {
      console.error("Failed to create WebSocket connection:", error);
      setSocket(null);

      return null;
    }
  }

  const handleSendMessage = () => {
    if (socket && inputMessage.trim()) {
      const message = {
        data_type: "chat",
        message: inputMessage,
      };

      socket.send(JSON.stringify(message));
      setInputMessage("");
    }
  };

  useEffect(() => {
    const ws = sockconnection();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  return (
    <div className="min-h-screen min-w-screen items-center justify-center flex flex-col">
      <h3>
        websocket {mysockid?.toString()} server time: {currentTime}
      </h3>

          <h4>
            total client are online : {totalclient}
          </h4>

      <div>
        <h3 className="font-bold">system messages</h3>
        <textarea
          readOnly
          className="w-96 h-48 border-2 border-gray-300 rounded-md p-2 m-2 focus:outline-none"
          placeholder="Messages will appear here..."
          value={systemMessages.join("\n")}
        />
      </div>

      <div>
        <h3 className="font-bold">chat messages</h3>
        <textarea
          readOnly
          className="w-96 h-48 border-2 border-gray-300 rounded-md p-2 m-2 focus:outline-none"
          placeholder="Messages will appear here..."
          value={chatMessages.join("\n")}
        />
      </div>

      <MessageInput
        value={inputMessage}
        onChange={(e) => setInputMessage(e.target.value)}
        onSend={handleSendMessage}
      />

      {socket?.readyState === WebSocket.OPEN ? "Connected" : "Disconnected"}
    </div>
  );
}

const MessageInput = memo(
  ({
    value,
    onChange,
    onSend,
  }: {
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onSend: () => void;
  }) => {
    return (
      <div>
        <input
          // id="myinput"
          type="text"
          value={value}
          onChange={onChange}
          className="border-2 border-gray-300 rounded-md p-2 m-2 focus:outline-none focus:border-blue-500"
          placeholder="Enter your message"
        />
        <button
          onClick={onSend}
          className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
        >
          Send
        </button>
      </div>
    );
  },
  (prevProps, nextProps) => {
    return prevProps.value === nextProps.value;
  }
);

export default App;
