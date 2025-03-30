import { useState, useEffect } from 'react';
import { Activity, CheckCircle, XCircle, Loader, ChevronRight, ChevronLeft } from 'lucide-react';

type Task = {
  id: string;
  name: string;
  status: 'running' | 'completed' | 'failed';
  progress: number;
};

type Props = {
  tasks: Task[];
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'running':
      return <Loader className="text-cyan-400 animate-spin" size={18} />;
    case 'completed':
      return <CheckCircle className="text-green-500" size={18} />;
    case 'failed':
      return <XCircle className="text-red-500" size={18} />;
    default:
      return <Activity className="text-gray-400" size={18} />;
  }
};

const getProgressColor = (status: string) => {
  switch (status) {
    case 'running':
      return 'bg-cyan-400';
    case 'completed':
      return 'bg-green-500';
    case 'failed':
      return 'bg-red-500';
    default:
      return 'bg-gray-500';
  }
};

const TaskList = ({ tasks }: Props) => {
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        setCollapsed(true);
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    return () => {
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, []);

  return (
    <div className={`fixed right-0 top-0 h-full transition-transform duration-300 ${collapsed ? 'translate-x-full' : 'translate-x-0'}`}>
      <div className="relative w-80 bg-gray-800 p-4 border-l border-gray-600 shadow-lg rounded-l-xl">
        <button 
          onClick={() => setCollapsed(!collapsed)} 
          className="absolute -left-8 top-4 bg-gray-700 text-gray-300 p-2 rounded-md border border-gray-600 hover:bg-gray-600 transition"
        >
          {collapsed ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
        </button>
        <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4 border-b border-gray-600 pb-2">Active Tasks</h2>
        <div className="space-y-4">
          {tasks.map((task) => (
            <div key={task.id} className="bg-gray-700 rounded-lg p-4 shadow-md border border-gray-600">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-gray-200 text-sm">{task.name}</span>
                {getStatusIcon(task.status)}
              </div>
              <div className="w-full bg-gray-600 rounded-full h-2 relative overflow-hidden border border-gray-500">
                <div 
                  className={`${getProgressColor(task.status)} h-2 rounded-full transition-all duration-700`}
                  style={{ width: `${task.progress}%` }}
                />
              </div>
              <span className="text-xs text-gray-400 mt-2 block">
                {task.progress}% {task.status === 'completed' ? '✅ Done' : task.status === 'failed' ? '❌ Failed' : '⏳ Processing...'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TaskList;
