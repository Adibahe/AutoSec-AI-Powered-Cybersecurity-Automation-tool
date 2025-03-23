// components/Sidebar.tsx
import React from 'react';
import { Shield, Search, Database, Terminal } from 'lucide-react';

const tools = [
  { name: 'Nmap Scanner', icon: <Search size={20} /> },
  { name: 'SQLMap', icon: <Database size={20} /> },
  { name: 'DNS Lookup', icon: <Terminal size={20} /> },
  { name: 'Security Audit', icon: <Shield size={20} /> }
];

const Sidebar = () => (
  <div className="w-64 bg-gray-800 p-4 border-r border-gray-700">
    <div className="flex items-center space-x-2 mb-8">
      <Shield className="text-cyan-500" size={24} />
      <h1 className="text-xl font-bold">SecureBot</h1>
    </div>
    <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4">Security Tools</h2>
    <div className="space-y-2">
      {tools.map((tool, index) => (
        <button key={index} className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors">
          {tool.icon}
          <span>{tool.name}</span>
        </button>
      ))}
    </div>
  </div>
);

export default Sidebar;
