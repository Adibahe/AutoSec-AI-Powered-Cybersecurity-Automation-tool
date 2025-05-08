import React, { useState } from "react";
import Sidebar from "./components/SideBar";
import ChatArea from "./components/ChatArea";
import TaskList from "./components/TaskList";
import InputForm from "./components/InputForm";

type Message =
  | {
      type: "user";
      content: string;
    }
  | {
      type: "bot";
      content: string;
      istool?: boolean;
      tool_out?: string;
      tool_outputs?: string[]; 
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

  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false); 

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    setLoading(true);
    setIsTyping(true); // ✅ Set isTyping to true before request
    console.log("Typing state:", isTyping); // Debugging log

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
      let partialChunk = "";

      if (reader) {
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          const text = decoder.decode(value, { stream: true });
          console.log("Raw SSE Response:", text);

          partialChunk += text;
          const jsonObjects = partialChunk.split("\n").filter(line => line.trim());

          for (const json of jsonObjects) {
            try {
              const parsed: BaseModel = JSON.parse(json);
              accumulatedMessage += parsed.data;

              setMessages(prev => {
                return prev.map((msg, index) => {
                  if (index === prev.length - 1 && msg.type === "bot") {
                    const updatedContent = { ...msg, content: accumulatedMessage };
              
                    if (parsed.istool && parsed.tool_out) {
                      const newToolOutputs = [...(msg.tool_outputs ?? []), parsed.tool_out];
                      return {
                        ...updatedContent,
                        tool_outputs: newToolOutputs,
                      };
                    }
              
                    return updatedContent;
                  }
              
                  return msg;
                });
              });
              
              
              

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
      setLoading(false);
      setIsTyping(false); 
      console.log("Typing state:", isTyping); // Debugging log
      controller.abort();
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <ChatArea messages={messages} isTyping={isTyping} /> {/* ✅ Pass isTyping */}
        <InputForm input={input} setInput={setInput} handleSubmit={handleSubmit} loading={loading} />
      </div>
      <TaskList tasks={tasks} />
    </div>
  );
}

export default Chat;
