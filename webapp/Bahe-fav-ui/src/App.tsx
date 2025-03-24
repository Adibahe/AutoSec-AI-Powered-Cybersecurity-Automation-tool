import React, { useState } from "react";
import Sidebar from "./components/SideBar";
import ChatArea from "./components/ChatArea";
import TaskList from "./components/TaskList";
import InputForm from "./components/InputForm";

type Message = {
  type: "user" | "bot";
  content: string;
};

type Task = {
  id: string;
  name: string;
  status: "running" | "completed" | "failed";
  progress: number;
};

function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [tasks] = useState<Task[]>([
    { id: "1", name: "Port Scanning", status: "running", progress: 45 },
    { id: "2", name: "Vulnerability Assessment", status: "completed", progress: 100 },
  ]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
  
    // Add user's message to the chat and create an empty bot message
    setMessages(prev => [...prev, { type: "user", content: input }, { type: "bot", content: "" }]);
    setInput("");
  
    // Create an AbortController to handle request cancellation
    const controller = new AbortController();
    const signal = controller.signal;
  
    try {
      const response = await fetch("http://127.0.0.1:5000/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: input }),
        signal,
      });
  
      if (!response.ok) throw new Error("Failed to connect to SSE stream");
  
      // Read the response as a stream
      const reader = response.body?.getReader();
      const decoder = new TextDecoder("utf-8");
  
      let accumulatedMessage = ""; // Stores the full bot response
  
      if (reader) {
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
  
          const text = decoder.decode(value, { stream: true });
          console.log("Raw SSE Response:", text); // Log full SSE response
  
          accumulatedMessage += text; // Append new chunk to accumulated message
  
          // Update the last bot message instead of adding a new one
          setMessages(prev => {
            return prev.map((msg, index) =>
              index === prev.length - 1 && msg.type === "bot"
                ? { ...msg, content: accumulatedMessage } // Update last bot message
                : msg
            );
          });
        }
      }
    } catch (error) {
      console.error("SSE Error:", error);
    } finally {
      controller.abort(); // Close the connection when finished
    }
  };
  
  
  return (
    <div className="flex h-screen bg-gray-900 text-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <ChatArea messages={messages} />
        <InputForm input={input} setInput={setInput} handleSubmit={handleSubmit} />
      </div>
      <TaskList tasks={tasks} />
    </div>
  );
}

export default Chat;
