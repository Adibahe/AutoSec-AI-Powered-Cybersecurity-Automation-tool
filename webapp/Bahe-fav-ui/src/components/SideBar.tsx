// components/Sidebar.tsx
import React from 'react';
import { Shield, Search, Database, Terminal } from 'lucide-react';



const tools = [


  { name: 'Nmap Scanner', icon: <Search size={20} />, link: 'https://nmap.org/book/intro.html' },


  { name: 'SQLMap', icon: <Database size={20} />, link: 'https://www.cyberbugs.in/post/what-is-sqlmap' },


  { name: 'DNS Lookup', icon: <Terminal size={20} />, link: 'https://denizhalil.com/2024/08/30/what-is-dns-lookup-nslookup-examples/' },


  { name: 'Security Audit', icon: <Shield size={20} />, link: 'https://qualysec.com/what-is-security-audit/' },


  { name: 'Exploitation', icon: <Shield size={20} />, link: 'https://example.com/exploitation' },

];

const Sidebar = () => (
  <div className="w-64 bg-gray-800 p-4 border-r border-gray-700">
    <div className="flex items-center justify-end space-x-2 mb-8 mt-4">
      <Shield className="text-cyan-500" size={28} />
      <h1 className="text-2xl font-bold">SecureBot</h1>
    </div>
    <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4">Security Tools we Support</h2>
    <div className="space-y-2">
      {tools.map((tool, index) => (
        <a
          key={index}
          href={tool.link}
          target="_blank"
          rel="noopener noreferrer"
          className="block"
        >
          <button className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors">
            {tool.icon}
            <span>{tool.name}</span>
          </button>
        </a>
      ))}
    </div>
  </div>
);

export default Sidebar;
