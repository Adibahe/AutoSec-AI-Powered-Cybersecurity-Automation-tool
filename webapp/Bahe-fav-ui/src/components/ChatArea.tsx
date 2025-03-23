// components/ChatArea.tsx
import React from 'react';

type Props = {
  messages: { type: 'user' | 'bot'; content: string }[];
};

const ChatArea = ({ messages }: Props) => (
  <div className="flex-1 overflow-y-auto p-6 space-y-4">
    {messages.map((message, index) => (
      <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
        <div className={`max-w-[70%] rounded-lg p-4 ${message.type === 'user' ? 'bg-cyan-600 text-white' : 'bg-gray-800 text-gray-100'}`}>{message.content}</div>
      </div>
    ))}
  </div>
);

export default ChatArea;