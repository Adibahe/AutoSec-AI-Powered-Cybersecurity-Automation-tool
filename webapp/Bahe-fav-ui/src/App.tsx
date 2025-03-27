import React, { useState } from "react";
import { Menu, X } from "lucide-react"; // Import icons for toggle button
import Sidebar from "./components/SideBar";
import ChatArea from "./components/ChatArea";
import TaskList from "./components/TaskList";
import InputForm from "./components/InputForm";

type Message = {
  type: "user";
  content: string;
} | {
  type: "bot";
  content: string;
  istool?: boolean;
  tool_out?: string;
};

type Task = {
  id: string;
  name: string;
  status: "running" | "completed" | "failed";
  progress: number;
};

type BaseModel = {
  data: string;
  istool: boolean;
  tool_out: string;
};

function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [tasks] = useState<Task[]>([
    { id: "1", name: "Port Scanning", status: "running", progress: 45 },
    { id: "2", name: "Vulnerability Assessment", status: "completed", progress: 100 },
  ]);
  const [isSidebarVisible, setIsSidebarVisible] = useState(true); // State to toggle sidebar visibility

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages(prev => [...prev, { type: "user", content: input }, { type: "bot", content: "" }]);
    setInput("");

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

      const reader = response.body?.getReader();
      const decoder = new TextDecoder("utf-8");

      let accumulatedMessage = "";
      let partialChunk = ""; // Store incomplete JSON data

      if (reader) {
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          const text = decoder.decode(value, { stream: true });
          console.log("Raw SSE Response:", text); // Debugging log

          partialChunk += text; // Append new chunk

          // Process each complete JSON line separately
          const jsonObjects = partialChunk.split("\n").filter(line => line.trim());

          for (const json of jsonObjects) {
            try {
              const parsed: BaseModel = JSON.parse(json);
              accumulatedMessage += parsed.data; // Append extracted data

              setMessages(prev =>
                prev.map((msg, index) =>
                  index === prev.length - 1 && msg.type === "bot"
                    ? {
                        ...msg,
                        content: accumulatedMessage,
                        ...(parsed.istool ? { istool: true, tool_out: parsed.tool_out } : {}),
                      }
                    : msg
                )
              );

              partialChunk = ""; 
            } catch (error) {
              console.warn("Waiting for full JSON object:", error);
            }
          }
        }
      }
    } catch (error) {
      console.error("SSE Error:", error);
    } finally {
      controller.abort();
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100">
      {/* Toggle Button */}
      <button
        className="absolute top-4 left-4 z-10 bg-gray-700 text-white p-2 rounded-full hover:bg-gray-600 transition"
        onClick={() => setIsSidebarVisible(!isSidebarVisible)}
      >
        {isSidebarVisible ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Sidebar */}
      {isSidebarVisible && <Sidebar />}

      {/* Main Content */}
      <div className={`flex-1 flex flex-col ${isSidebarVisible ? "ml-64" : "ml-0"} transition-all`}>
        <ChatArea messages={messages} />
        <InputForm input={input} setInput={setInput} handleSubmit={handleSubmit} />
      </div>

      <TaskList tasks={tasks} />
    </div>
  );
}

export default Chat;
