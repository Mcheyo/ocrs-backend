// frontend/src/services/chatbotApi.js

// Simple API client for the AI Advisor chatbot.
// This matches your backend endpoint:
//
// POST http://127.0.0.1:5001/api/chatbot/message
// body: { "message": "<user text>" }

export async function sendChatMessage(message) {
  try {
    const response = await fetch("http://127.0.0.1:5001/api/chatbot/message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      console.error(
        "Chatbot API HTTP error:",
        response.status,
        response.statusText
      );
      return "Sorry, the AI Advisor is temporarily unavailable (HTTP error).";
    }

    const data = await response.json();

    // Adjust this if your backend uses a different field
    if (typeof data === "string") return data;
    if (data.reply) return data.reply;
    if (data.message) return data.message;

    console.warn("Chatbot API: unexpected response format", data);
    return "I received a response from the server, but it was in an unexpected format.";
  } catch (err) {
    console.error("Chatbot API network error:", err);
    return "Network error: I couldn’t reach the AI Advisor service.";
  }
}

// Also provide a default export just in case someone imports default.
export default { sendChatMessage };

