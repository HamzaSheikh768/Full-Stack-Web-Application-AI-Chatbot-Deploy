import { TaskSummary } from './TaskSummary';
import { cn } from '@/lib/utils';

interface ChatMessageProps {
  content: string;
  role: 'user' | 'assistant';
  taskData?: any; // Optional task data to display summary
  className?: string;
}

export function ChatMessage({ content, role, taskData, className }: ChatMessageProps) {
  return (
    <div className={`flex ${role === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div
        className={cn(
          `max-w-[80%] rounded-lg px-4 py-2`,
          role === 'user'
            ? 'bg-blue-600 text-white rounded-br-none'
            : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-bl-none',
          className
        )}
      >
        {content}
        
        {/* Display task summary if task data is available */}
        {taskData && (
          <div className="mt-2">
            <TaskSummary
              title={taskData.title || taskData.name || 'Untitled Task'}
              description={taskData.description}
              priority={taskData.priority}
              tags={taskData.tags}
              dueDate={taskData.due_date || taskData.dueAt}
              completed={taskData.completed || taskData.is_completed}
            />
          </div>
        )}
      </div>
    </div>
  );
}