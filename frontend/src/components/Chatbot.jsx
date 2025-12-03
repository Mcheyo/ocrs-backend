import React, { useState } from "react";
import { sendChatMessage } from "../services/chatbotApi";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      from: "bot",
      text:
        "Hi! I'm the OCRS helper bot. Ask me about registration, courses, or how OCRS works.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg(null);

    const trimmed = input.trim();
    if (!trimmed) return;

    const userMessage = {
      id: Date.now(),
      from: "user",
      text: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(trimmed);

      const botMessage = {
        id: Date.now() + 1,
        from: "bot",
        text: data.reply,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      setErrorMsg("Sorry, I couldn't reach the OCRS chatbot.");
      const botMessage = {
        id: Date.now() + 2,
        from: "bot",
        text:
          "There was a problem contacting the server. Please try again in a moment.",
      };
      setMessages((prev) => [...prev, botMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "600px",
        margin: "0 auto",
        border: "1px solid #ddd",
        borderRadius: "8px",
        display: "flex",
        flexDirection: "column",
        height: "500px",
      }}
    >
      <div
        style={{
          padding: "12px 16px",
          borderBottom: "1px solid #eee",
          fontWeight: 600,
          backgroundColor: "#f7f7f7",
        }}
      >
        OCRS Chatbot
      </div>

      <div
        style={{
          flex: 1,
          padding: "12px",
          overflowY: "auto",
          backgroundColor: "#fafafa",
        }}
      >
        {messages.map((m) => (
          <div
            key={m.id}
            style={{
              display: "flex",
              justifyContent: m.from === "user" ? "flex-end" : "flex-start",
              marginBottom: "8px",
            }}
          >
            <div
              style={{
                maxWidth: "80%",
                padding: "8px 12px",
                borderRadius: "16px",
                backgroundColor:
                  m.from === "user" ? "#007bff" : "#e4e6eb",
                color: m.from === "user" ? "#fff" : "#000",
                fontSize: "14px",
                whiteSpace: "pre-wrap",
              }}
            >
              {m.text}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ fontSize: "12px", color: "#666" }}>
            The bot is typing…
          </div>
        )}
      </div>

      {errorMsg && (
        <div
          style={{
            color: "red",
            fontSize: "12px",
            padding: "4px 12px",
          }}
        >
          {errorMsg}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          borderTop: "1px solid #eee",
          padding: "8px",
          gap: "8px",
        }}
      >
        <input
          type="text"
          value={input}
          placeholder="Ask me how to register, search courses, add/drop, etc."
          onChange={(e) => setInput(e.target.value)}
          style={{
            flex: 1,
            padding: "8px 10px",
            borderRadius: "16px",
            border: "1px solid #ccc",
            fontSize: "14px",
          }}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          style={{
            padding: "8px 16px",
            borderRadius: "16px",
            border: "none",
            cursor: loading ? "not-allowed" : "pointer",
            opacity: loading || !input.trim() ? 0.6 : 1,
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default Chatbot;

