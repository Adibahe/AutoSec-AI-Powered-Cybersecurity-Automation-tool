// components/InputForm.tsx
import React from 'react';
import { ChevronRight } from 'lucide-react';

type Props = {
  input: string;
  setInput: (input: string) => void;
  handleSubmit: (e: React.FormEvent) => void;
};

const InputForm = ({ input, setInput, handleSubmit }: Props) => (
  <form onSubmit={handleSubmit} className="p-4 border-t border-gray-700">
    <div className="flex space-x-4">
      <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type your security command..." className="flex-1 bg-gray-800 text-gray-100 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500" />
      <button type="submit" className="bg-cyan-600 text-white px-6 py-2 rounded-lg hover:bg-cyan-700 transition-colors">
        <ChevronRight size={20} />
      </button>
    </div>
  </form>
);

export default InputForm;
