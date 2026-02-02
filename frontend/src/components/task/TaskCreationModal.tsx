'use client';

import { useState } from 'react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '../ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '../ui/dialog';
import { Label } from '../ui/label';
import { Plus } from 'lucide-react';
import { taskApi } from '@/lib/api';
import { Task as UiTask } from '@/types/task';

interface TaskCreationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (task: Omit<UiTask, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => void;
}

export function TaskCreationModal({ isOpen, onClose, onCreate }: TaskCreationModalProps) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium' as 'low' | 'medium' | 'high',
    due_date: '',
    tags: '',
    recurrence: 'none' as 'none' | 'daily' | 'weekly',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newTask = {
      title: formData.title,
      description: formData.description || undefined,
      priority: formData.priority,
      due_date: formData.due_date || undefined,
      is_completed: false, // Default to not completed
      recurrence_pattern: formData.recurrence, // Use recurrence field
    };

    try {
      // Use the API to create the task
      await taskApi.createTask(newTask);
      // Close the modal after successful creation
      onClose();
      // Reset form data
      setFormData({
        title: '',
        description: '',
        priority: 'medium',
        due_date: '',
        tags: '',
        recurrence: 'none',
      });
    } catch (error) {
      console.error('Error creating task:', error);
      alert('Failed to create task. Please try again.');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePriorityChange = (value: 'low' | 'medium' | 'high') => {
    setFormData(prev => ({ ...prev, priority: value }));
  };

  const handleRecurrenceChange = (value: 'none' | 'daily' | 'weekly') => {
    setFormData(prev => ({ ...prev, recurrence: value }));
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Create New Task</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="title">Title *</Label>
            <Input
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              placeholder="Task title"
            />
          </div>
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Task description"
              className="min-h-[100px]"
            />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="priority">Priority</Label>
              <Select value={formData.priority} onValueChange={handlePriorityChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="due_date">Due Date</Label>
              <Input
                id="due_date"
                name="due_date"
                type="date"
                value={formData.due_date}
                onChange={handleChange}
              />
            </div>
          </div>
          <div>
            <Label htmlFor="tags">Tags</Label>
            <Input
              id="tags"
              name="tags"
              value={formData.tags}
              onChange={handleChange}
              placeholder="Comma separated tags"
            />
          </div>
          <div>
            <Label htmlFor="recurrence">Recurrence</Label>
            <Select value={formData.recurrence} onValueChange={handleRecurrenceChange}>
              <SelectTrigger>
                <SelectValue placeholder="Recurrence" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="none">None</SelectItem>
                <SelectItem value="daily">Daily</SelectItem>
                <SelectItem value="weekly">Weekly</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <DialogFooter className="sm:justify-start">
            <Button type="submit" className="w-full">
              <Plus className="mr-2 h-4 w-4" /> Create Task
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}