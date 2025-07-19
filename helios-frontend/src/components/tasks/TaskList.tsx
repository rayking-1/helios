import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Task } from '../../types';
import { TaskItem } from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdate?: (id: string, updates: Partial<Task>) => void;
  onTaskDelete?: (id: string) => void;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onTaskUpdate,
  onTaskDelete,
}) => {
  return (
    <div className="space-y-2">
      <AnimatePresence mode="popLayout">
        {tasks.map((task, index) => (
          <motion.div
            key={task.id}
            layout
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ delay: index * 0.05 }}
          >
            <TaskItem
              task={task}
              onUpdate={onTaskUpdate}
              onDelete={onTaskDelete}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}; 