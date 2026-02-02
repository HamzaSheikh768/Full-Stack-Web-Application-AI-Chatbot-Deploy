'use client';

import { useState } from 'react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Checkbox } from '../ui/checkbox';
import { Card, CardContent, CardFooter } from '../ui/card';
import { Calendar, Flag, Tag, Edit3, Trash2, Save, X } from 'lucide-react';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '../ui/select';
import { isOverdue } from '@/lib/utils';
import { Task as ApiTask } from '@/lib/api';
import { taskApi } from '@/lib/api';

interface TaskItemProps {
  task: ApiTask;
  onUpdate: (task: ApiTask) => void;
  onDelete: (taskId: string) => void;
  onToggleComplete: (taskId: string, completed: boolean) => void;
}

export function TaskItem({ task, onUpdate, onDelete, onToggleComplete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTask, setEditedTask] = useState({
    title: task.title,
    description: task.description || "",
    priority: task.priority,
    due_date: task.due_date || "",
    status: task.status || "pending", // Add required status field
    type: task.type || "daily", // Add required type field
  });

  const handleSave = async () => {
    try {
      // Update the task using the authenticated API
      const updatedTask = await taskApi.updateTask(task.id, {
        title: editedTask.title,
        description: editedTask.description,
        priority: editedTask.priority as 'low' | 'medium' | 'high',
        due_date: editedTask.due_date || undefined,
      });

      onUpdate(updatedTask);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating task:', error);
      alert('Failed to update task. Please try again.');
    }
  };

  const handleCancel = () => {
    setEditedTask({
      title: task.title,
      description: task.description || "",
      priority: task.priority,
      due_date: task.due_date || "",
      status: task.status || "pending",
      type: task.type || "daily",
    });
    setIsEditing(false);
  };

  return (
    <Card className={`transition-all duration-200 ${
      task.status === "completed"
        ? "bg-green-50/50 dark:bg-green-900/20 border-green-200 dark:border-green-800"
        : "bg-white/80 dark:bg-gray-800/80 border-gray-200 dark:border-gray-600"
    } ${isOverdue(task.due_date || "") ? "border-l-4 border-l-red-500" : ""}`}>
      {isEditing ? (
        // Edit mode
        <CardContent className="pt-6">
          <div className="space-y-4">
            <Input
              value={editedTask.title}
              onChange={(e) => setEditedTask({...editedTask, title: e.target.value})}
              placeholder="Task title"
            />
            <Textarea
              value={editedTask.description}
              onChange={(e) => setEditedTask({...editedTask, description: e.target.value})}
              placeholder="Description"
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Select
                value={editedTask.priority}
                onValueChange={(value) => setEditedTask({...editedTask, priority: value as any})}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="LOW">Low</SelectItem>
                  <SelectItem value="MEDIUM">Medium</SelectItem>
                  <SelectItem value="HIGH">High</SelectItem>
                </SelectContent>
              </Select>
              <Input
                type="date"
                value={editedTask.due_date}
                onChange={(e) => setEditedTask({...editedTask, due_date: e.target.value})}
              />
            </div>
          </div>
        </CardContent>
      ) : (
        // View mode
        <>
          <CardContent className="pt-6">
            <div className="flex flex-col sm:flex-row sm:items-start space-y-3 sm:space-y-0 sm:space-x-4">
              <Checkbox
                checked={task.status === "completed"}
                onCheckedChange={async (checked) => {
                  try {
                    // Toggle completion using the authenticated API
                    const updatedTask = await taskApi.updateTaskCompletion(task.id, Boolean(checked));
                    onToggleComplete(task.id, Boolean(checked));
                  } catch (error) {
                    console.error('Error updating task completion:', error);
                    alert('Failed to update task completion. Please try again.');
                  }
                }}
                className="mt-1 self-start"
              />
              <div className="flex-1 min-w-0">
                <h3 className={`font-medium break-words ${
                  task.status === "completed"
                    ? "line-through text-gray-500 dark:text-gray-400"
                    : "text-gray-800 dark:text-white"
                }`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-sm text-gray-600 dark:text-gray-300 mt-1 break-words">
                    {task.description}
                  </p>
                )}
                <div className="flex flex-wrap items-center gap-2 mt-2">
                  <Badge variant={task.priority === "high" ? "destructive" : task.priority === "medium" ? "default" : "secondary"}>
                    {task.priority.toLowerCase()}
                  </Badge>
                  {task.due_date && (
                    <div className="flex items-center text-xs text-gray-500 dark:text-gray-400 whitespace-nowrap">
                      <Calendar className="h-3 w-3 mr-1" />
                      {new Date(task.due_date).toLocaleDateString()}
                      {isOverdue(task.due_date) && (
                        <span className="ml-1 text-red-500">(Overdue)</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </>
      )}
      <CardFooter className="flex justify-between border-t border-gray-200 dark:border-gray-700 pt-4">
        <div className="flex space-x-2">
          {isEditing ? (
            <>
              <Button size="sm" onClick={handleSave}>
                <Save className="h-4 w-4 mr-2" /> Save
              </Button>
              <Button size="sm" variant="outline" onClick={handleCancel}>
                <X className="h-4 w-4 mr-2" /> Cancel
              </Button>
            </>
          ) : (
            <>
              <Button size="sm" variant="outline" onClick={() => setIsEditing(true)}>
                <Edit3 className="h-4 w-4 mr-2" /> Edit
              </Button>
              <Button size="sm" variant="outline" onClick={async () => {
                if (confirm('Are you sure you want to delete this task?')) {
                  try {
                    // Delete the task using the authenticated API
                    await taskApi.deleteTask(task.id);
                    onDelete(task.id);
                  } catch (error) {
                    console.error('Error deleting task:', error);
                    alert('Failed to delete task. Please try again.');
                  }
                }
              }}>
                <Trash2 className="h-4 w-4 mr-2" /> Delete
              </Button>
            </>
          )}
        </div>
      </CardFooter>
    </Card>
  );
}