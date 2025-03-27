import React from 'react';
import { Activity } from 'lucide-react';

type Task = {
  id: string;
  name: string;
  status: 'running' | 'completed' | 'failed';
  progress: number;
};

type Props = {
  tasks: Task[];
};

const TaskList = ({ tasks }: Props) => (
  <div className="w-80 bg-gray-800 p-4 border-l border-gray-700">
    <h2 className="text-sm font-semibold text-gray-400 uppercase mb-4">Active Tasks</h2>
    <div className="space-y-4">
      {tasks.map((task) => (
        <div key={task.id} className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium">{task.name}</span>
            <Activity className="text-cyan-500" size={16} />
          </div>
          <div className="w-full bg-gray-600 rounded-full h-2">
            <div className="bg-cyan-500 h-2 rounded-full transition-all duration-500" style={{ width: `${task.progress}%` }} />
          </div>
          <span className="text-sm text-gray-400 mt-2 block">{task.progress}% Complete</span>
        </div>
      ))}
    </div>
  </div>
);

export default TaskList;
