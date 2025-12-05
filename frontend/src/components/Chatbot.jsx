// Chatbot.jsx
import React, { useState, useRef, useEffect } from "react";
import { MessageCircle, X, Send } from "lucide-react";

export default function Chatbot({ currentUser }) {
  // Start CLOSED so you only see the bubble
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "bot",
      text:
        "Hi! I’m the OCRS AI Advisor. I can help with registration and system " +
        "questions (how to register, drop, course status, login issues) and " +
        "also with academic planning (what to take next, prerequisites, GPA, etc.). " +
        "What would you like help with?",
    },
  ]);

  const bottomRef = useRef(null);

  // Always scroll to newest message
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen]);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || isSending) return;

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsSending(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:5001/api/chatbot/message",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: trimmed,
            user: currentUser
              ? {
                  id: currentUser.id,
                  name: currentUser.name,
                  role: currentUser.role,
                  major: currentUser.major,
                  currentGPA: currentUser.currentGPA,
                }
              : null,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Chatbot HTTP error ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();

      const botText =
        data?.data?.reply ||
        data?.reply ||
        data?.message ||
        "I’m not sure I understood that. Try asking about registration steps, dropping a course, prerequisites, or course planning.";

      const botMessage = {
        id: Date.now() + 1,
        sender: "bot",
        text: botText,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error("AI Advisor error:", err);
      const fallbackMessage = {
        id: Date.now() + 1,
        sender: "bot",
        text:
          "Sorry, I couldn’t reach the AI Advisor service. " +
          "Make sure the backend is running on http://127.0.0.1:5001. " +
          "You can still use the Courses tab and enroll/drop buttons on this page.",
      };
      setMessages((prev) => [...prev, fallbackMessage]);
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* Bubble when closed */}
      {!isOpen && (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          className="fixed bottom-4 right-4 z-40 bg-indigo-600 text-white rounded-full px-5 py-3 shadow-lg hover:bg-indigo-700 flex items-center space-x-2"
        >
          <MessageCircle className="h-5 w-5" />
          <span className="text-sm font-medium">AI Advisor</span>
        </button>
      )}

      {/* Popup window */}
      {isOpen && (
        <div className="fixed bottom-4 right-4 z-40 w-full max-w-md">
          <div className="bg-white rounded-xl shadow-2xl flex flex-col h-[420px]">
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-2 bg-indigo-600 text-white rounded-t-xl">
              <div className="flex items-center space-x-2">
                <MessageCircle className="h-5 w-5" />
                <div className="flex flex-col">
                  <span className="font-semibold text-sm">AI Advisor</span>
                  <span className="text-xs text-indigo-100">
                    OCRS Help &amp; Academic Guidance
                  </span>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="hover:bg-indigo-700 rounded-full p-1"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-3 py-2 bg-gray-50">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={
                    "mb-2 flex " +
                    (msg.sender === "user" ? "justify-end" : "justify-start")
                  }
                >
                  <div
                    className={
                      "max-w-[80%] rounded-lg px-3 py-2 text-sm " +
                      (msg.sender === "user"
                        ? "bg-indigo-600 text-white"
                        : "bg-white text-gray-800 border border-gray-200")
                    }
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
              <div ref={bottomRef} />
            </div>

            {/* Input */}
            <div className="border-t border-gray-200 px-3 py-2 bg-white rounded-b-xl">
              <div className="flex items-center space-x-2">
                <textarea
                  rows={1}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  className="flex-1 resize-none border border-gray-300 rounded-md px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Ask how to register, drop courses, check prerequisites, or plan next classes…"
                />
                <button
                  type="button"
                  onClick={handleSend}
                  disabled={isSending || !input.trim()}
                  className={
                    "p-2 rounded-md text-white flex items-center justify-center " +
                    (isSending || !input.trim()
                      ? "bg-gray-300 cursor-not-allowed"
                      : "bg-indigo-600 hover:bg-indigo-700")
                  }
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
