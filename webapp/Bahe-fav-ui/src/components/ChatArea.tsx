import React, { useState, useEffect, useRef } from "react";
import { Terminal, ChevronDown, ChevronUp } from "lucide-react";
import TypingIndicator from "./TypingIndicator";

interface Message {
  type: "user" | "bot";
  content: string;
  istool?: boolean;
  tool_out?: string;
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

  const toggleToolOutput = (index: number) => {
    setExpandedTools((prev) =>
      prev.includes(index.toString())
        ? prev.filter((id) => id !== index.toString())
        : [...prev, index.toString()]
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
            {message.istool && message.tool_out && (
              <div className="mt-3">
                <button
                  onClick={() => toggleToolOutput(index)}
                  className="flex items-center gap-2 text-sm text-blue-400 hover:text-white transition-colors"
                >
                  <Terminal className="w-4 h-4" />
                  <span>Tool Output</span>
                  {expandedTools.includes(index.toString()) ? (
                    <ChevronUp className="w-4 h-4" />
                  ) : (
                    <ChevronDown className="w-4 h-4" />
                  )}
                </button>
                {expandedTools.includes(index.toString()) && (
                  <pre className="mt-2 p-4 bg-gray-800 text-gray-200 font-mono text-sm rounded-lg overflow-x-auto max-h-40 border border-gray-600">
                    {message.tool_out}
                  </pre>
                )}
              </div>
            )}
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
