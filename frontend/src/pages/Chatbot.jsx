import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Chatbot() {
  const navigate = useNavigate();

  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [sessionId, setSessionId] = useState("");
  const [location, setLocation] = useState(null);

  // Session ID
  useEffect(() => {
    let id = localStorage.getItem("session_id");

    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("session_id", id);
    }

    setSessionId(id);
  }, []);

  // Get Current Location
  useEffect(() => {
    if (!navigator.geolocation) return;

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          lat: position.coords.latitude,
          lon: position.coords.longitude,
        });

        console.log("Location:", position.coords.latitude, position.coords.longitude);
      },
      (err) => {
        console.log("Location Permission Denied", err);
      }
    );
  }, []);

  const sendMessage = async () => {
    if (!message.trim()) return;

    if (!sessionId) {
      console.log("Session not ready");
      return;
    }

    const userMessage = message;

    // Show user message
    setChat((prev) => [
      ...prev,
      {
        sender: "user",
        text: userMessage,
      },
    ]);

    setMessage("");

    try {
      const payload = {
        message: userMessage,
        session_id: sessionId,
      };

      // If user asks weather and GPS available
      const q = userMessage.toLowerCase();

      if (
        location &&
        (
          q === "weather" ||
          q === "today weather" ||
          q === "current weather" ||
          q === "wether"
        )
      ) {
        payload.lat = location.lat;
        payload.lon = location.lon;
      }

      const response = await api.post("/chat", payload);

      console.log("Backend Response:", response.data);

      // Bot Reply
  const reply = response.data.reply;

  let botReply = "";

    if (typeof reply === "string") {
  botReply = reply;
    } else if (reply && typeof reply === "object") {
    botReply = JSON.stringify(reply);
  } else {
  botReply = String(reply ?? "");
}

console.log("BOT REPLY:", botReply);

setChat((prev) => [
  ...prev,
  {
    sender: "bot",
    text: botReply,
  },
]);

      // Auto Navigation
      if (
        response.data.success &&
        response.data.type === "navigation" &&
        response.data.page
      ) {
        console.log("Navigate:", response.data.page);

        setTimeout(() => {
          navigate(response.data.page);
        }, 1200);
      }
    } catch (error) {
      console.error(error);

    let errorMessage = "❌ Unable to connect to server.";

    if (error.response) {
  const errorReply = error.response.data.reply;

  if (typeof errorReply === "string") {
    errorMessage = errorReply;
  } else {
    errorMessage = JSON.stringify(
      error.response.data
    );
  }
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

          <p className="mt-2">
            Ask anything about farming, crops, diseases and weather.
          </p>
        </div>

        {/* Chat */}

        <div className="h-[500px] overflow-y-auto p-5 space-y-4">

          {chat.length === 0 && (
            <div className="text-center text-gray-500 mt-10">
              🌾 Ask about crops, fertilizer, irrigation,
              diseases, weather and farming.
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
                className={`max-w-[75%] whitespace-pre-wrap px-4 py-3 rounded-2xl ${
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