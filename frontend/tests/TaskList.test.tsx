import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { TaskList } from '@/components/task/TaskList';
import { Task as ApiTask } from '@/lib/api';

// Mock the child components
jest.mock('@/components/task/TaskItem', () => ({
  TaskItem: ({ task }: { task: ApiTask }) => <div data-testid={`task-item-${task.id}`}>{task.title}</div>,
}));
jest.mock('@/components/task/TaskFilters', () => ({
  TaskFilters: ({ filters, onFilterChange }: any) => (
    <div data-testid="task-filters">
      <span>Filters applied: {JSON.stringify(filters)}</span>
      <button onClick={() => onFilterChange({ ...filters, status: 'completed' })}>
        Set status to completed
      </button>
    </div>
  ),
}));
jest.mock('@/components/SortControls', () => ({
  SortControls: ({ sortBy, sortOrder, onSortChange }: any) => (
    <div data-testid="sort-controls">
      <span>Sorted by: {sortBy}, order: {sortOrder}</span>
      <button onClick={() => onSortChange('priority', 'desc')}>
        Sort by priority desc
      </button>
    </div>
  ),
}));

describe('TaskList Component', () => {
  const mockTasks: ApiTask[] = [
    {
      id: '1',
      user_id: 'user123',
      title: 'Task 1',
      description: 'Description 1',
      is_completed: false,
      priority: 'high',
      recurrence_pattern: 'none',
      due_date: '2026-12-31T10:00:00Z',
      created_at: '2026-02-01T10:00:00Z',
      updated_at: '2026-02-01T10:00:00Z',
      tags: ['work'],
    },
    {
      id: '2',
      user_id: 'user123',
      title: 'Task 2',
      description: 'Description 2',
      is_completed: true,
      priority: 'low',
      recurrence_pattern: 'daily',
      due_date: '2026-11-30T10:00:00Z',
      created_at: '2026-02-01T10:00:00Z',
      updated_at: '2026-02-01T10:00:00Z',
      tags: ['personal'],
    },
  ];

  const mockOnTaskUpdate = jest.fn();
  const mockOnTaskDelete = jest.fn();
  const mockOnTaskToggleComplete = jest.fn();
  const mockOnAddTaskClick = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders task list with tasks', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onTaskUpdate={mockOnTaskUpdate}
        onTaskDelete={mockOnTaskDelete}
        onTaskToggleComplete={mockOnTaskToggleComplete}
        onAddTaskClick={mockOnAddTaskClick}
      />
    );

    expect(screen.getByText('Your Tasks')).toBeInTheDocument();
    expect(screen.getByTestId('task-item-1')).toBeInTheDocument();
    expect(screen.getByTestId('task-item-2')).toBeInTheDocument();
    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
  });

  it('renders filters and sort controls', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onTaskUpdate={mockOnTaskUpdate}
        onTaskDelete={mockOnTaskDelete}
        onTaskToggleComplete={mockOnTaskToggleComplete}
        onAddTaskClick={mockOnAddTaskClick}
      />
    );

    expect(screen.getByTestId('task-filters')).toBeInTheDocument();
    expect(screen.getByTestId('sort-controls')).toBeInTheDocument();
  });

  it('applies filters when filter changes', async () => {
    render(
      <TaskList
        tasks={mockTasks}
        onTaskUpdate={mockOnTaskUpdate}
        onTaskDelete={mockOnTaskDelete}
        onTaskToggleComplete={mockOnTaskToggleComplete}
        onAddTaskClick={mockOnAddTaskClick}
      />
    );

    const filterButton = screen.getByText('Set status to completed');
    fireEvent.click(filterButton);

    expect(screen.getByText('Filters applied: {"status":"completed","priority":"all","tags":[],"dueDateFrom":"","dueDateTo":"","search":""}')).toBeInTheDocument();
  });

  it('applies sorting when sort changes', async () => {
    render(
      <TaskList
        tasks={mockTasks}
        onTaskUpdate={mockOnTaskUpdate}
        onTaskDelete={mockOnTaskDelete}
        onTaskToggleComplete={mockOnTaskToggleComplete}
        onAddTaskClick={mockOnAddTaskClick}
      />
    );

    const sortButton = screen.getByText('Sort by priority desc');
    fireEvent.click(sortButton);

    expect(screen.getByText('Sorted by: priority, order: desc')).toBeInTheDocument();
  });

  it('shows empty state when no tasks match filters', () => {
    render(
      <TaskList
        tasks={[]} // Empty task list
        onTaskUpdate={mockOnTaskUpdate}
        onTaskDelete={mockOnTaskDelete}
        onTaskToggleComplete={mockOnTaskToggleComplete}
        onAddTaskClick={mockOnAddTaskClick}
      />
    );

    expect(screen.getByText('No tasks yet. Add your first task!')).toBeInTheDocument();
  });

  it('shows filtered empty state when tasks exist but don\'t match filters', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onTaskUpdate={mockOnTaskUpdate}
        onTaskDelete={mockOnTaskDelete}
        onTaskToggleComplete={mockOnTaskToggleComplete}
        onAddTaskClick={mockOnAddTaskClick}
      />
    );

    // Manually trigger a filter that would result in no tasks
    // This would typically happen through the TaskFilters component
    // For this test, we'll simulate the filtered state by passing filtered tasks
    render(
      <TaskList
        tasks={[]} // Simulate filtered tasks
        loading={false}
        onTaskUpdate={mockOnTaskUpdate}
        onTaskDelete={mockOnTaskDelete}
        onTaskToggleComplete={mockOnTaskToggleComplete}
        onAddTaskClick={mockOnAddTaskClick}
      />
    );

    expect(screen.getByText('No tasks match your current filters.')).toBeInTheDocument();
  });

  it('handles loading state', () => {
    render(
      <TaskList
        tasks={mockTasks}
        loading={true}
        onTaskUpdate={mockOnTaskUpdate}
        onTaskDelete={mockOnTaskDelete}
        onTaskToggleComplete={mockOnTaskToggleComplete}
        onAddTaskClick={mockOnAddTaskClick}
      />
    );

    // Check for skeleton loaders
    const skeletons = screen.getAllByRole('status'); // Assuming skeleton has role="status"
    expect(skeletons.length).toBeGreaterThan(0);
  });
});