import React from 'react';

const TypingIndicator = () => {
  return (
    <div className="flex space-x-2 p-3 bg-gray-800 rounded-lg max-w-[100px]">
      <div className="w-2.5 h-2.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
      <div className="w-2.5 h-2.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '200ms' }}></div>
      <div className="w-2.5 h-2.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '400ms' }}></div>
    </div>
  );
};

export default TypingIndicator;