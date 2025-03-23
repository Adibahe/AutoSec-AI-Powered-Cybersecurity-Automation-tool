import React, { useState } from 'react';
import { Terminal, Search, Database, Shield, Activity, ChevronRight } from 'lucide-react';

interface Message {
  type: 'user' | 'bot';
  content: string;
}

interface Task {
  id: string;
  name: string;
  status: 'running' | 'completed' | 'failed';
  progress: number;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [tasks] = useState<Task[]>([
    { id: '1', name: 'Port Scanning', status: 'running', progress: 45 },
    { id: '2', name: 'Vulnerability Assessment', status: 'completed', progress: 100 }
  ]);

  const tools = [
    { name: 'Nmap Scanner', icon: <Search size={20} /> },
    { name: 'SQLMap', icon: <Database size={20} /> },
    { name: 'DNS Lookup', icon: <Terminal size={20} /> },
    { name: 'Security Audit', icon: <Shield size={20} /> }
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages([...messages, { type: 'user', content: input }]);
    // Simulate bot response
    setTimeout(() => {
      setMessages(prev => [...prev, { type: 'bot', content: 'Processing your security request...' }]);
    }, 1000);
    setInput('');
  };

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100">
      {/* Left Sidebar */}
      <div className="w-64 bg-gray-800 p-4 border-r border-gray-700">
        <div className="flex items-center space-x-2 mb-8">
          <Shield className="text-cyan-500" size={24} />
          <h1 className="text-xl font-bold">SecureBot</h1>
        </div>
        <div className="space-y-4">
          <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4">Security Tools</h2>
          <div className="space-y-2">
            {tools.map((tool, index) => (
              <button
                key={index}
                className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors"
              >
                {tool.icon}
                <span>{tool.name}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] rounded-lg p-4 ${
                  message.type === 'user'
                    ? 'bg-cyan-600 text-white'
                    : 'bg-gray-800 text-gray-100'
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="p-4 border-t border-gray-700">
          <div className="flex space-x-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your security command..."
              className="flex-1 bg-gray-800 text-gray-100 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
            <button
              type="submit"
              className="bg-cyan-600 text-white px-6 py-2 rounded-lg hover:bg-cyan-700 transition-colors"
            >
              <ChevronRight size={20} />
            </button>
          </div>
        </form>
      </div>

      {/* Right Sidebar */}
      <div className="w-80 bg-gray-800 p-4 border-l border-gray-700">
        <div>
          <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4">Active Tasks</h2>
          <div className="space-y-4">
            {tasks.map((task) => (
              <div key={task.id} className="bg-gray-700 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium">{task.name}</span>
                  <Activity className="text-cyan-500" size={16} />
                </div>
                <div className="w-full bg-gray-600 rounded-full h-2">
                  <div
                    className="bg-cyan-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${task.progress}%` }}
                  />
                </div>
                <span className="text-sm text-gray-400 mt-2 block">
                  {task.progress}% Complete
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;