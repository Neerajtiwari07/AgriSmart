import { useState } from "react";
import api from "../services/api";

function Chatbot() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;

    setChat((prev) => [
      ...prev,
      {
        sender: "user",
        text: userMessage,
      },
    ]);

    setMessage("");

    try {
      const response = await api.post("/chat", {
        message: userMessage,
      });

      setChat((prev) => [
        ...prev,
        {
          sender: "bot",
          text: response.data.reply,
        },
      ]);
    } catch (error) {
      console.error(error);

      setChat((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "❌ Unable to connect to server.",
        },
      ]);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg">

        {/* Header */}
        <div className="bg-green-700 text-white p-5 rounded-t-2xl">
          <h1 className="text-3xl font-bold">
            🤖 AgriSmart AI Chatbot
          </h1>
          <p>Ask any farming related question</p>
        </div>

        {/* Chat Area */}
        <div className="h-[500px] overflow-y-auto p-5 space-y-4">

          {chat.length === 0 && (
            <div className="text-gray-500 text-center mt-10">
              🌾 Ask about crops, fertilizers, diseases, irrigation, etc.
            </div>
          )}

          {chat.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.sender === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >
              <div
                className={`max-w-md p-3 rounded-xl ${
                  msg.sender === "user"
                    ? "bg-green-700 text-white"
                    : "bg-gray-200 text-black"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}

        </div>

        {/* Input */}
        <div className="p-4 border-t flex gap-3">

          <input
            type="text"
            placeholder="Type your question..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="flex-1 border p-3 rounded-lg"
            onKeyDown={(e) =>
              e.key === "Enter" && sendMessage()
            }
          />

          <button
            onClick={sendMessage}
            className="bg-green-700 text-white px-6 rounded-lg"
          >
            Send
          </button>

        </div>

      </div>
    </div>
  );
}

export default Chatbot;