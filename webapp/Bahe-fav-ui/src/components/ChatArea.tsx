import React, { useState } from "react";
import { Terminal, ChevronDown, ChevronUp } from "lucide-react";

interface Message {
  type: "user" | "bot";
  content: string;
  istool?: boolean;
  tool_out?: string;
}

interface Props {
  messages: Message[];
}

const ChatArea: React.FC<Props> = ({ messages }) => {
  const [expandedTools, setExpandedTools] = useState<string[]>([]);

  const toggleToolOutput = (index: number) => {
    setExpandedTools((prev) =>
      prev.includes(index.toString())
        ? prev.filter((id) => id !== index.toString())
        : [...prev, index.toString()]
    );
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.map((message, index) => (
        <div key={index} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
          <div className={`max-w-[70%] rounded-lg p-4 ${message.type === "user" ? "bg-cyan-600 text-white" : "bg-gray-800 text-gray-100"}`}>
            <pre className="whitespace-pre-wrap font-sans">{message.content}</pre>

            {/* Show Tool Output Button ONLY if this message has tool output */}
            {message.istool && message.tool_out && (
              <div className="mt-3">
                <button
                  onClick={() => toggleToolOutput(index)}
                  className="flex items-center gap-2 text-sm text-gray-300 hover:text-white transition-colors"
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
                  <pre className="mt-2 p-3 bg-black rounded text-sm text-gray-300 overflow-x-auto">
                    {message.tool_out}
                  </pre>
                )}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatArea;
