"use client";
import React from "react";

function MainComponent() {
  const [selectedTool, setSelectedTool] = useState("nmap");
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const tools = [
    { id: "nmap", name: "NMAP Scanner", icon: "🔍" },
    { id: "password", name: "Password Cracker", icon: "🔑" },
    { id: "exploit", name: "Exploitation Tool", icon: "⚡" },
    { id: "lookup", name: "Lookup Handler", icon: "🔎" },
  ];
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/process-command", {
        method: "POST",
        body: JSON.stringify({ tool: selectedTool, prompt }),
      });

      const data = await response.json();
      setResult(data.result);
    } catch (err) {
      setError("Failed to process command. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900">
      <div className="w-64 bg-gray-800 p-4">
        <div className="text-green-500 text-xl font-bold mb-8">
          Security Toolkit
        </div>
        <nav>
          {tools.map((tool) => (
            <button
              key={tool.id}
              onClick={() => setSelectedTool(tool.id)}
              className={`w-full text-left p-3 rounded mb-2 flex items-center ${
                selectedTool === tool.id
                  ? "bg-gray-700 text-green-500"
                  : "text-gray-300 hover:bg-gray-700"
              }`}
            >
              <span className="mr-2">{tool.icon}</span>
              {tool.name}
            </button>
          ))}
        </nav>
      </div>

      <div className="flex-1 p-8">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl font-bold text-green-500 mb-8">
            {tools.find((t) => t.id === selectedTool)?.name}
          </h1>
          <form onSubmit={handleSubmit} className="mb-8">
            <div className="mb-4">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter your command..."
                className="w-full h-32 p-4 bg-gray-800 text-gray-100 rounded border border-gray-700 focus:border-green-500 focus:ring-1 focus:ring-green-500"
              />
            </div>
            <button
              type="submit"
              disabled={isLoading}
              className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 disabled:opacity-50"
            >
              {isLoading ? "Processing..." : "Execute"}
            </button>
          </form>

          {error && (
            <div className="bg-red-900/50 border border-red-700 text-red-100 p-4 rounded mb-4">
              {error}
            </div>
          )}

          {isLoading && (
            <div className="animate-pulse bg-gray-800 h-40 rounded"></div>
          )}

          {result && !isLoading && (
            <div className="bg-gray-800 p-4 rounded">
              <pre className="text-gray-100 whitespace-pre-wrap">{result}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MainComponent;