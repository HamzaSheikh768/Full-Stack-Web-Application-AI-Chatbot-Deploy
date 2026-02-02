'use client';

import React from 'react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Task } from '@/lib/api'; // Use the Task type from the API
import { format } from 'date-fns';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (id: string, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
  loadingIds?: string[]; // IDs of tasks currently being processed
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onToggleComplete,
  onEdit,
  onDelete,
  loadingIds = []
}) => {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500 dark:text-gray-400">No tasks found. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <Card key={task.id} className="transition-all duration-200 hover:shadow-md">
          <CardHeader className="p-4 pb-2">
            <div className="flex items-start space-x-3">
              <div className="flex items-center space-x-2 pt-1">
                <Checkbox
                  id={`completed-${task.id}`}
                  checked={task.is_completed}
                  onCheckedChange={(checked) => {
                    onToggleComplete(task.id, Boolean(checked));
                  }}
                  disabled={loadingIds.includes(task.id)} // Disable during loading
                />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className={`font-medium truncate ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-900 dark:text-gray-100'}`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
                    {task.description}
                  </p>
                )}
              </div>
            </div>
          </CardHeader>

          <CardContent className="p-4 pt-2">
            <div className="flex flex-wrap gap-2">
              <Badge variant={task.priority === 'high' ? 'destructive' : task.priority === 'medium' ? 'default' : 'secondary'}>
                {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
              </Badge>

              {task.recurrence_pattern && (
                <Badge variant="outline">
                  {task.recurrence_pattern.charAt(0).toUpperCase() + task.recurrence_pattern.slice(1)}
                </Badge>
              )}

              {task.due_date && (
                <Badge variant="outline">
                  Due: {format(new Date(task.due_date), 'MMM dd, yyyy')}
                </Badge>
              )}
            </div>
          </CardContent>

          <CardFooter className="p-4 pt-2 flex justify-end space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onEdit(task)}
              disabled={loadingIds.includes(task.id)}
            >
              Edit
            </Button>
            <Button
              variant="destructive"
              size="sm"
              onClick={() => onDelete(task.id)}
              disabled={loadingIds.includes(task.id)}
            >
              {loadingIds.includes(task.id) ? 'Deleting...' : 'Delete'}
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  );
};

export { TaskList };