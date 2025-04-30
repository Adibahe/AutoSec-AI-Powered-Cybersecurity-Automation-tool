import React, { useState, useEffect, useRef } from "react";
import { Terminal, ChevronDown, ChevronUp } from "lucide-react";
import TypingIndicator from "./TypingIndicator";

interface Message {
  type: "user" | "bot";
  content: string;
  tool_outputs?: string[]; 
}


interface Props {
  messages: Message[];
  isTyping?: boolean;
}

const ChatArea: React.FC<Props> = ({ messages, isTyping = false }) => {
  const [expandedTools, setExpandedTools] = useState<string[]>([]);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Automatically scroll to the bottom when messages update
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

 const toggleToolOutput = (id: string) => {
  setExpandedTools((prev) =>
    prev.includes(id)
      ? prev.filter((existingId) => existingId !== id)
      : [...prev, id]
  );
};


  return (
    <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.type === "user" ? "justify-end" : "justify-start"} w-full`}
        >
          <div
            className={`max-w-[75%] p-4 rounded-2xl shadow-md transition-colors ${
              message.type === "user"
                ? "bg-transparent border border-blue-500 text-white self-end"
                : "bg-gray-700 text-gray-100 self-start"
            }`}
          >
            <p className="whitespace-pre-wrap font-sans text-base md:text-lg leading-relaxed">
              {message.content}
            </p>

            {/* Tool Output Section */}
            {message.tool_outputs && message.tool_outputs.map((toolOut, i) => (
  <div key={i} className="mt-3 max-w-full">
    <button
      onClick={() => toggleToolOutput(`${index}-${i}`)}
      className="flex items-center gap-2 text-sm text-blue-400 hover:text-white transition-colors"
    >
      <Terminal className="w-4 h-4" />
      <span>Tool Output #{i + 1}</span>
      {expandedTools.includes(`${index}-${i}`) ? (
        <ChevronUp className="w-4 h-4" />
      ) : (
        <ChevronDown className="w-4 h-4" />
      )}
    </button>
    {expandedTools.includes(`${index}-${i}`) && (
      <pre className="mt-2 p-4 bg-gray-800 text-gray-200 font-mono text-sm rounded-lg border border-gray-600 overflow-x-auto overflow-y-auto max-h-[400px] max-w-full">
        {toolOut}
      </pre>
    )}
  </div>
))}

          </div>
        </div>
      ))}

      {/* Typing Indicator */}
      {isTyping && (
        <div className="flex justify-start">
          <TypingIndicator />
        </div>
      )}
    </div>
  );
};

export default ChatArea;
