import { Activity, CheckCircle, XCircle, Loader } from 'lucide-react';

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
      return <Loader className="text-yellow-400 animate-spin" size={18} />;
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
      return 'bg-yellow-400';
    case 'completed':
      return 'bg-green-500';
    case 'failed':
      return 'bg-red-500';
    default:
      return 'bg-gray-500';
  }
};

const TaskList = ({ tasks }: Props) => (
  <div className="w-80 bg-gray-800 p-4 border-l border-gray-700">
    <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4">Active Tasks</h2>
    <div className="space-y-4">
      {tasks.map((task) => (
        <div key={task.id} className="bg-gray-700 rounded-lg p-4 shadow-md">
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium text-gray-200 text-sm">{task.name}</span>
            {getStatusIcon(task.status)}
          </div>
          <div className="w-full bg-gray-600 rounded-full h-2 relative overflow-hidden">
            <div 
              className={`${getProgressColor(task.status)} h-2 rounded-full transition-all duration-700`}
              style={{ width: `${task.progress}%` }}
            />
          </div>
          <span className="text-xs text-gray-400 mt-2 block">
            {task.progress}% {task.status === 'completed' ? 'Done' : task.status === 'failed' ? '❌ Failed' : 'Processing...'}
          </span>
        </div>
      ))}
    </div>
  </div>
);

export default TaskList;
