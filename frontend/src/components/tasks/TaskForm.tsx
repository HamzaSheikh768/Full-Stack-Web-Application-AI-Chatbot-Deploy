'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface TaskFormData {
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high';
  type?: 'daily' | 'weekly' | 'monthly' | 'yearly' | 'none';
  dueDate?: string;
}

interface TaskFormProps {
  onSubmit: (data: TaskFormData) => void;
  onCancel?: () => void;
  initialData?: Partial<TaskFormData>;
  isSubmitting?: boolean;
}

const TaskForm: React.FC<TaskFormProps> = ({ onSubmit, onCancel, initialData, isSubmitting = false }) => {
  const [formData, setFormData] = useState<TaskFormData>({
    title: initialData?.title || '',
    description: initialData?.description || '',
    priority: initialData?.priority || 'medium',
    type: initialData?.type?.toLowerCase() as 'daily' | 'weekly' | 'monthly' | 'yearly' | 'none' || 'none',
    dueDate: initialData?.dueDate || '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleSelectChange = (name: keyof TaskFormData) => (value: string) => {
    setFormData(prev => ({ ...prev, [name]: value as any }));

    // Clear error when user selects an option
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.trim().length > 200) {
      newErrors.title = 'Title must be 200 characters or less';
    }

    if (formData.description && formData.description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>{initialData ? 'Edit Task' : 'Create New Task'}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Title Field */}
          <div>
            <Label htmlFor="title">Title *</Label>
            <Input
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Enter task title"
              className={errors.title ? 'border-red-500' : ''}
            />
            {errors.title && <p className="text-red-500 text-sm mt-1">{errors.title}</p>}
          </div>

          {/* Description Field */}
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter task description (optional)"
              className={errors.description ? 'border-red-500' : ''}
            />
            {errors.description && <p className="text-red-500 text-sm mt-1">{errors.description}</p>}
          </div>

          {/* Priority Field */}
          <div>
            <Label htmlFor="priority">Priority</Label>
            <Select value={formData.priority} onValueChange={handleSelectChange('priority')}>
              <SelectTrigger id="priority" className={errors.priority ? 'border-red-500' : ''}>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="low">Low</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="high">High</SelectItem>
              </SelectContent>
            </Select>
            {errors.priority && <p className="text-red-500 text-sm mt-1">{errors.priority}</p>}
          </div>

          {/* Type Field */}
          <div>
            <Label htmlFor="type">Type</Label>
            <Select value={formData.type?.toUpperCase() || 'NONE'} onValueChange={(value) => handleSelectChange('type')(value.toLowerCase())}>
              <SelectTrigger id="type">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="NONE">None</SelectItem>
                <SelectItem value="DAILY">Daily</SelectItem>
                <SelectItem value="WEEKLY">Weekly</SelectItem>
                <SelectItem value="MONTHLY">Monthly</SelectItem>
                <SelectItem value="YEARLY">Yearly</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Due Date Field */}
          <div>
            <Label htmlFor="dueDate">Due Date</Label>
            <Input
              id="dueDate"
              name="dueDate"
              type="datetime-local"
              value={formData.dueDate}
              onChange={handleChange}
              placeholder="Select due date (optional)"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-2 pt-4">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : (initialData ? 'Update Task' : 'Create Task')}
            </Button>
            {onCancel && (
              <Button type="button" variant="outline" onClick={onCancel} disabled={isSubmitting}>
                Cancel
              </Button>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export { TaskForm, type TaskFormData };