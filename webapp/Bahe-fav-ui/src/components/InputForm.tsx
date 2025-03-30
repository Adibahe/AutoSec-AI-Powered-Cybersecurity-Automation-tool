import React, { useRef, useEffect } from "react";
import { ChevronRight, Loader2 } from "lucide-react";

type Props = {
  input: string;
  setInput: (input: string) => void;
  handleSubmit: (e: React.FormEvent) => void;
  loading: boolean;
};

const InputForm = ({ input, setInput, handleSubmit, loading }: Props) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"; // Reset height
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; // Adjust height dynamically
    }
  }, [input]);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value.trimStart()); // Removes leading spaces
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() !== "") handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border-t border-gray-700 bg-gray-900">
      <div className="flex items-end space-x-4">
        {/* Dynamic Input Field */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type your command..."
            className="w-full bg-gray-800 text-gray-100 text-lg font-mono px-5 py-4 rounded-lg 
                       focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-shadow 
                       disabled:bg-gray-700 resize-none overflow-y-auto max-h-40 shadow-md"
            disabled={loading}
          />
        </div>

        {/* Send Button - Fixed Size */}
        <button
          type="submit"
          className="h-12 w-14 bg-cyan-600 text-white rounded-lg flex items-center justify-center 
                     hover:bg-cyan-700 transition-colors disabled:bg-gray-600 shadow-lg"
          disabled={loading || input.trim() === ""}
        >
          {loading ? <Loader2 className="animate-spin" size={24} /> : <ChevronRight size={24} />}
        </button>
      </div>
    </form>
  );
};

export default InputForm;
