import { useState, useEffect } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

function Chatbot() {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [sessionId, setSessionId] = useState("");

  // Create Session ID (Only Once)
  useEffect(() => {
    let id = localStorage.getItem("session_id");

    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("session_id", id);
    }

    setSessionId(id);
  }, []);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;

    // Show user message immediately
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
        session_id: sessionId,
      });

      setChat((prev) => [
        ...prev,
        {
          sender: "bot",
          text: response.data.reply,
        },
      ]);
    // Navigation Response
    if (response.data.type === "navigation") {

      setTimeout(() => {

       navigate(response.data.page);

    }, 1500);

}

    } catch (error) {
      console.error("Axios Error:", error);

      let errorMessage = "❌ Unable to connect to server.";

      if (error.response) {
        console.log("Status:", error.response.status);
        console.log("Data:", error.response.data);

        errorMessage =
          error.response.data.reply ||
          JSON.stringify(error.response.data);
      } else if (error.message) {
        errorMessage = error.message;
      }

      setChat((prev) => [
        ...prev,
        {
          sender: "bot",
          text: errorMessage,
        },
      ]);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg overflow-hidden">

        {/* Header */}
        <div className="bg-green-700 text-white p-5">
          <h1 className="text-3xl font-bold">
            🤖 AgriSmart AI Chatbot
          </h1>

          <p className="mt-1">
            Ask any farming related question
          </p>
        </div>

        {/* Chat Area */}
        <div className="h-[500px] overflow-y-auto p-5 space-y-4">

          {chat.length === 0 && (
            <div className="text-center text-gray-500 mt-10">
              🌾 Ask about crops, fertilizer, irrigation,
              weather, diseases and farming.
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
                className={`max-w-[70%] whitespace-pre-wrap px-4 py-3 rounded-2xl ${
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

        {/* Input Area */}
        <div className="border-t p-4 flex gap-3">

          <input
            type="text"
            placeholder="Type your farming question..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            className="flex-1 border rounded-lg p-3 outline-none focus:ring-2 focus:ring-green-600"
          />

          <button
            onClick={sendMessage}
            className="bg-green-700 hover:bg-green-800 text-white px-6 rounded-lg"
          >
            Send
          </button>

        </div>
      </div>
    </div>
  );
}

export default Chatbot;