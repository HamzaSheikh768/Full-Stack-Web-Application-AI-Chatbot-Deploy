'use client';

import React from 'react';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { ArrowUpAZ, ArrowDownZA, Calendar, Flag, Clock } from 'lucide-react';

interface SortOption {
  id: string;
  label: string;
  icon: React.JSX.Element;
}

interface SortControlsProps {
  sortBy: string;
  sortOrder: 'asc' | 'desc';
  onSortChange: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
}

export function SortControls({ sortBy, sortOrder, onSortChange }: SortControlsProps) {
  const sortOptions: SortOption[] = [
    { id: 'created_at', label: 'Created Date', icon: <Clock className="h-4 w-4 mr-2" /> },
    { id: 'due_at', label: 'Due Date', icon: <Calendar className="h-4 w-4 mr-2" /> },
    { id: 'priority', label: 'Priority', icon: <Flag className="h-4 w-4 mr-2" /> },
    { id: 'title', label: 'Title', icon: <ArrowUpAZ className="h-4 w-4 mr-2" /> },
  ];

  const handleSortByChange = (value: string) => {
    onSortChange(value, sortOrder);
  };

  const handleSortOrderChange = () => {
    const newOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    onSortChange(sortBy, newOrder);
  };

  const selectedOption = sortOptions.find(option => option.id === sortBy) || sortOptions[0];

  return (
    <div className="flex flex-wrap items-center gap-2 p-2 bg-gray-50 dark:bg-gray-800 rounded-lg">
      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Sort by:</span>
      
      <Select value={sortBy} onValueChange={handleSortByChange}>
        <SelectTrigger className="w-[160px]">
          <SelectValue placeholder="Select sort option" />
        </SelectTrigger>
        <SelectContent>
          {sortOptions.map((option) => (
            <SelectItem key={option.id} value={option.id}>
              <div className="flex items-center">
                {option.icon}
                {option.label}
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      
      <Button
        variant="outline"
        size="sm"
        onClick={handleSortOrderChange}
        className="flex items-center"
      >
        {sortOrder === 'asc' ? (
          <>
            <ArrowUpAZ className="h-4 w-4 mr-2" />
            Ascending
          </>
        ) : (
          <>
            <ArrowDownZA className="h-4 w-4 mr-2" />
            Descending
          </>
        )}
      </Button>
    </div>
  );
}