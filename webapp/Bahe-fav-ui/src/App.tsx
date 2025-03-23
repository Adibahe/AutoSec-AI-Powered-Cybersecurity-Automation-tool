import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/SideBar';
import ChatArea from './components/ChatArea';
import TaskList from './components/TaskList';
import InputForm from './components/InputForm';
import Test from './components/Test';

type Message = {
  type: 'user' | 'bot';
  content: string;
};

type Task = {
  id: string;
  name: string;
  status: 'running' | 'completed' | 'failed';
  progress: number;
};

function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [tasks] = useState<Task[]>([
    { id: '1', name: 'Port Scanning', status: 'running', progress: 45 },
    { id: '2', name: 'Vulnerability Assessment', status: 'completed', progress: 100 }
  ]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages([...messages, { type: 'user', content: input }]);
    setTimeout(() => {
      setMessages(prev => [...prev, { type: 'bot', content: 'Processing your security request...' }]);
    }, 1000);
    setInput('');
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

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/chat" element={<Chat />} />
        <Route path="/test" element={<Test />} />
        <Route path="*" element={<Navigate to="/chat" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
