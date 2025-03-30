import { useState } from "react";
import { Shield, Search, Database, Terminal, ChevronLeft, ChevronRight } from "lucide-react";

const tools = [
  { name: "Nmap Scanner", icon: <Search size={20} />, link: "https://nmap.org/book/intro.html" },
  { name: "SQLMap", icon: <Database size={20} />, link: "https://www.cyberbugs.in/post/what-is-sqlmap" },
  { name: "DNS Lookup", icon: <Terminal size={20} />, link: "https://denizhalil.com/2024/08/30/what-is-dns-lookup-nslookup-examples/" },
  { name: "Security Audit", icon: <Shield size={20} />, link: "https://qualysec.com/what-is-security-audit/" },
  { name: "Exploitation", icon: <Shield size={20} />, link: "https://example.com/exploitation" },
];

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className="flex">
      {/* Sidebar */}
      <div
        className={`h-screen bg-gray-950 border-r border-gray-800 shadow-lg flex flex-col transition-all duration-300 relative ${
          isCollapsed ? "w-16 p-3" : "w-64 p-6"
        }`}
      >
        {/* Toggle Button (Centered on Sidebar Border) */}
        <button
          className="absolute top-1/2 -right-4 transform -translate-y-1/2 bg-gray-800 p-2 rounded-full shadow-md text-gray-300 hover:text-white hover:bg-cyan-600 transition"
          onClick={() => setIsCollapsed(!isCollapsed)}
        >
          {isCollapsed ? <ChevronRight size={24} /> : <ChevronLeft size={24} />}
        </button>

        {/* Header */}
        <div className="flex items-center space-x-3 mb-8">
          <Shield className="text-cyan-400" size={32} />
          {!isCollapsed && <h1 className="text-3xl font-extrabold text-gray-100">AutoSec</h1>}
        </div>

        {/* Tools Section */}
        {!isCollapsed && (
          <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4">Security Tools</h2>
        )}

        <div className="space-y-3 flex-1">
          {tools.map((tool, index) => (
            <a key={index} href={tool.link} target="_blank" rel="noopener noreferrer">
              <button
                className={`w-full flex items-center ${
                  isCollapsed ? "justify-center p-4" : "space-x-3 px-5 py-3"
                } rounded-lg bg-gray-900 hover:bg-cyan-600 transition-all text-gray-300 hover:text-white shadow-sm group mb-2 text-lg font-medium`}
              >
                <span className="text-cyan-400 group-hover:text-white">{tool.icon}</span>
                {!isCollapsed && <span>{tool.name}</span>}
              </button>
            </a>
          ))}
        </div>

        {/* Footer */}
        {!isCollapsed && (
          <div className="mt-auto text-center text-xs text-gray-500">
            <p>&copy; 2025 AutoSec</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
