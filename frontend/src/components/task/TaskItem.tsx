'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Calendar, Flag, Tag as TagIcon, Edit3, Trash2, Save, X, Bell } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
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
    tags: task.tags || [], // Added tags
    remind_at: task.remind_at || "", // Added reminder
    is_recurring: task.is_recurring || false, // Added recurring flag
    recurrence_pattern_details: task.recurrence_pattern_details || null, // Added recurrence details
    next_due_date: task.next_due_date || "", // Added next due date
    status: task.status || "pending", // Add required status field
    type: task.type || "daily", // Add required type field
  });

  const [newTag, setNewTag] = useState(""); // For adding new tags

  const handleSave = async () => {
    try {
      // Update the task using the authenticated API
      const updatedTask = await taskApi.updateTask(task.id, {
        title: editedTask.title,
        description: editedTask.description,
        priority: editedTask.priority as 'low' | 'medium' | 'high',
        due_date: editedTask.due_date || undefined,
        tags: editedTask.tags, // Include tags in update
        remind_at: editedTask.remind_at || undefined, // Include reminder in update
        is_recurring: editedTask.is_recurring, // Include recurring flag in update
        recurrence_pattern_details: editedTask.recurrence_pattern_details, // Include recurrence details in update
        next_due_date: editedTask.next_due_date || undefined, // Include next due date in update
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
      tags: task.tags || [], // Reset tags
      remind_at: task.remind_at || "", // Reset reminder
      is_recurring: task.is_recurring || false, // Reset recurring flag
      recurrence_pattern_details: task.recurrence_pattern_details || null, // Reset recurrence details
      next_due_date: task.next_due_date || "", // Reset next due date
      status: task.status || "pending",
      type: task.type || "daily",
    });
    setNewTag("");
    setIsEditing(false);
  };

  const addTag = () => {
    if (newTag.trim() && !editedTask.tags.includes(newTag.trim())) {
      setEditedTask({
        ...editedTask,
        tags: [...editedTask.tags, newTag.trim()]
      });
      setNewTag("");
    }
  };

  const removeTag = (tagToRemove: string) => {
    setEditedTask({
      ...editedTask,
      tags: editedTask.tags.filter(tag => tag !== tagToRemove)
    });
  };

  // Determine priority badge variant and icon
  const getPriorityVariant = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'destructive';
      case 'medium':
        return 'default';
      case 'low':
        return 'secondary';
      default:
        return 'secondary';
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return <Flag className="h-3 w-3 mr-1" />;
      case 'medium':
        return <Flag className="h-3 w-3 mr-1 opacity-70" />;
      case 'low':
        return <Flag className="h-3 w-3 mr-1 opacity-40" />;
      default:
        return <Flag className="h-3 w-3 mr-1" />;
    }
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
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                </SelectContent>
              </Select>
              <Input
                type="datetime-local"
                value={editedTask.due_date}
                onChange={(e) => setEditedTask({...editedTask, due_date: e.target.value})}
              />
            </div>
            
            {/* Tags section */}
            <div>
              <div className="flex items-center mb-2">
                <TagIcon className="h-4 w-4 mr-2" />
                <label className="text-sm font-medium">Tags</label>
              </div>
              <div className="flex flex-wrap gap-2 mb-2">
                {editedTask.tags.map((tag, index) => (
                  <Badge key={index} variant="secondary" className="flex items-center">
                    {tag}
                    <button 
                      type="button" 
                      onClick={() => removeTag(tag)}
                      className="ml-2 text-xs rounded-full hover:bg-destructive hover:text-destructive-foreground"
                    >
                      ×
                    </button>
                  </Badge>
                ))}
              </div>
              <div className="flex gap-2">
                <Input
                  value={newTag}
                  onChange={(e) => setNewTag(e.target.value)}
                  placeholder="Add a tag..."
                  onKeyDown={(e) => e.key === 'Enter' && addTag()}
                />
                <Button type="button" size="sm" variant="outline" onClick={addTag}>Add</Button>
              </div>
            </div>
            
            {/* Reminder section */}
            <div>
              <div className="flex items-center mb-2">
                <Bell className="h-4 w-4 mr-2" />
                <label className="text-sm font-medium">Reminder</label>
              </div>
              <Input
                type="datetime-local"
                value={editedTask.remind_at}
                onChange={(e) => setEditedTask({...editedTask, remind_at: e.target.value})}
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
                
                {/* Priority, tags, due date, and reminder info */}
                <div className="flex flex-wrap items-center gap-2 mt-2">
                  {/* Priority indicator with icon */}
                  <Badge variant={getPriorityVariant(task.priority)}>
                    {getPriorityIcon(task.priority)}
                    {task.priority.toLowerCase()}
                  </Badge>
                  
                  {/* Tags */}
                  {task.tags && task.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {task.tags.map((tag, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          <TagIcon className="h-2.5 w-2.5 mr-1" />
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  )}
                  
                  {/* Due date */}
                  {task.due_date && (
                    <div className={`flex items-center text-xs whitespace-nowrap ${
                      isOverdue(task.due_date) 
                        ? "text-red-500 dark:text-red-400 font-semibold" 
                        : "text-gray-500 dark:text-gray-400"
                    }`}>
                      <Calendar className="h-3 w-3 mr-1" />
                      {new Date(task.due_date).toLocaleDateString()}
                      {isOverdue(task.due_date) && (
                        <span className="ml-1 animate-pulse">(OVERDUE)</span>
                      )}
                    </div>
                  )}
                  
                  {/* Reminder */}
                  {task.remind_at && (
                    <div className="flex items-center text-xs text-blue-500 dark:text-blue-400 whitespace-nowrap">
                      <Bell className="h-3 w-3 mr-1" />
                      {new Date(task.remind_at).toLocaleString()}
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