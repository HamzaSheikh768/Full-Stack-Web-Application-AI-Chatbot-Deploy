import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { TaskItem } from '@/components/task/TaskItem';
import { Task as ApiTask } from '@/lib/api';

// Mock the taskApi module
jest.mock('@/lib/api', () => ({
  taskApi: {
    updateTask: jest.fn(),
    deleteTask: jest.fn(),
    updateTaskCompletion: jest.fn(),
  },
}));

describe('TaskItem Component', () => {
  const mockTask: ApiTask = {
    id: '1',
    user_id: 'user123',
    title: 'Test Task',
    description: 'Test Description',
    is_completed: false,
    priority: 'medium',
    recurrence_pattern: 'none',
    due_date: '2026-12-31T10:00:00Z',
    created_at: '2026-02-01T10:00:00Z',
    updated_at: '2026-02-01T10:00:00Z',
    tags: ['work', 'important'],
    remind_at: '2026-12-30T09:00:00Z',
    is_recurring: false,
    recurrence_pattern_details: null,
    next_due_date: null,
  };

  const mockOnUpdate = jest.fn();
  const mockOnDelete = jest.fn();
  const mockOnToggleComplete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders task details correctly', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText('medium')).toBeInTheDocument();
    expect(screen.getByText('work')).toBeInTheDocument();
    expect(screen.getByText('important')).toBeInTheDocument();
  });

  it('toggles completion status when checkbox is clicked', async () => {
    const { taskApi } = require('@/lib/api');
    const updatedTask = { ...mockTask, is_completed: true };
    (taskApi.updateTaskCompletion as jest.MockedFunction<any>).mockResolvedValue(updatedTask);

    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    const checkbox = screen.getByRole('checkbox');
    fireEvent.click(checkbox);

    await waitFor(() => {
      expect(taskApi.updateTaskCompletion).toHaveBeenCalledWith(mockTask.id, true);
      expect(mockOnToggleComplete).toHaveBeenCalledWith(mockTask.id, true);
    });
  });

  it('enters edit mode when edit button is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Test Description')).toBeInTheDocument();
  });

  it('updates task when save is clicked in edit mode', async () => {
    const { taskApi } = require('@/lib/api');
    const updatedTask = { ...mockTask, title: 'Updated Task' };
    (taskApi.updateTask as jest.MockedFunction<any>).mockResolvedValue(updatedTask);

    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    // Enter edit mode
    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    // Change the title
    const titleInput = screen.getByDisplayValue('Test Task');
    fireEvent.change(titleInput, { target: { value: 'Updated Task' } });

    // Click save
    const saveButton = screen.getByText('Save');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(taskApi.updateTask).toHaveBeenCalledWith(mockTask.id, {
        title: 'Updated Task',
        description: 'Test Description',
        priority: 'medium',
        due_date: '2026-12-31T10:00:00Z',
        tags: ['work', 'important'],
        remind_at: '2026-12-30T09:00:00Z',
      });
      expect(mockOnUpdate).toHaveBeenCalledWith(updatedTask);
    });
  });

  it('cancels edit mode when cancel is clicked', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    // Enter edit mode
    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    // Verify we're in edit mode
    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument();

    // Click cancel
    const cancelButton = screen.getByText('Cancel');
    fireEvent.click(cancelButton);

    // Verify we're back in view mode
    expect(screen.queryByDisplayValue('Test Task')).not.toBeInTheDocument();
    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('deletes task when delete button is confirmed', async () => {
    const { taskApi } = require('@/lib/api');
    (taskApi.deleteTask as jest.MockedFunction<any>).mockResolvedValue({ success: true, message: 'Deleted' });

    // Mock window.confirm to return true
    window.confirm = jest.fn(() => true);

    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(window.confirm).toHaveBeenCalledWith('Are you sure you want to delete this task?');
      expect(taskApi.deleteTask).toHaveBeenCalledWith(mockTask.id);
      expect(mockOnDelete).toHaveBeenCalledWith(mockTask.id);
    });
  });

  it('shows overdue indicator when task is overdue', () => {
    const overdueTask = {
      ...mockTask,
      due_date: '2020-01-01T10:00:00Z', // Past date
    };

    render(
      <TaskItem
        task={overdueTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        onToggleComplete={mockOnToggleComplete}
      />
    );

    expect(screen.getByText('(Overdue)')).toBeInTheDocument();
  });
});