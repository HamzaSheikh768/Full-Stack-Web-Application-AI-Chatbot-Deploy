import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Calendar } from '@/components/ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { cn } from '@/lib/utils';
import { format } from 'date-fns';
import { CalendarIcon, X, Tag, Flag, Clock, Filter } from 'lucide-react';

interface TaskFiltersProps {
  filters: {
    status: string;
    priority: string;
    tags: string[];
    dueDateFrom: string;
    dueDateTo: string;
    search: string;
  };
  onFilterChange: (filters: any) => void;
  availableTags: string[];
}

export function TaskFilters({ filters, onFilterChange, availableTags }: TaskFiltersProps) {
  const [newTag, setNewTag] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleStatusChange = (status: string) => {
    onFilterChange({ ...filters, status });
  };

  const handlePriorityChange = (priority: string) => {
    onFilterChange({ ...filters, priority });
  };

  const handleTagToggle = (tag: string) => {
    const newTags = filters.tags.includes(tag)
      ? filters.tags.filter(t => t !== tag)
      : [...filters.tags, tag];
    
    onFilterChange({ ...filters, tags: newTags });
  };

  const addTag = () => {
    if (newTag.trim() && !availableTags.includes(newTag.trim())) {
      const newAvailableTags = [...availableTags, newTag.trim()];
      const newTags = [...filters.tags, newTag.trim()];
      onFilterChange({ ...filters, tags: newTags });
      setNewTag('');
    }
  };

  const removeTag = (tag: string) => {
    const newTags = filters.tags.filter(t => t !== tag);
    onFilterChange({ ...filters, tags: newTags });
  };

  const handleDueDateFromChange = (date: Date | undefined) => {
    onFilterChange({ 
      ...filters, 
      dueDateFrom: date ? date.toISOString() : '' 
    });
  };

  const handleDueDateToChange = (date: Date | undefined) => {
    onFilterChange({ 
      ...filters, 
      dueDateTo: date ? date.toISOString() : '' 
    });
  };

  const handleSearchChange = (search: string) => {
    onFilterChange({ ...filters, search });
  };

  const handleClearFilters = () => {
    onFilterChange({
      status: 'all',
      priority: 'all',
      tags: [],
      dueDateFrom: '',
      dueDateTo: '',
      search: ''
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2 items-center">
        <Select
          value={filters.status}
          onValueChange={handleStatusChange}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Tasks</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="completed">Completed</SelectItem>
          </SelectContent>
        </Select>

        <Select
          value={filters.priority}
          onValueChange={handlePriorityChange}
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Priority" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Priorities</SelectItem>
            <SelectItem value="low">Low Priority</SelectItem>
            <SelectItem value="medium">Medium Priority</SelectItem>
            <SelectItem value="high">High Priority</SelectItem>
          </SelectContent>
        </Select>

        <Input
          placeholder="Search tasks..."
          value={filters.search}
          onChange={(e) => handleSearchChange(e.target.value)}
          className="max-w-xs"
        />

        <Button variant="outline" size="sm" onClick={() => setShowAdvanced(!showAdvanced)}>
          <Filter className="h-4 w-4 mr-2" />
          {showAdvanced ? 'Hide Filters' : 'More Filters'}
        </Button>

        {(filters.status !== 'all' || filters.priority !== 'all' || filters.tags.length > 0 || filters.search) && (
          <Button variant="outline" size="sm" onClick={handleClearFilters}>
            <X className="h-4 w-4 mr-2" />
            Clear
          </Button>
        )}
      </div>

      {showAdvanced && (
        <div className="space-y-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <h3 className="font-medium flex items-center">
            <Filter className="h-4 w-4 mr-2" />
            Advanced Filters
          </h3>
          
          <div className="space-y-2">
            <Label className="flex items-center">
              <Tag className="h-3.5 w-3.5 mr-1.5" />
              Tags
            </Label>
            <div className="flex flex-wrap gap-2">
              {filters.tags.map((tag) => (
                <Badge key={tag} variant="secondary" className="flex items-center">
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
            <div className="flex gap-2 mt-2">
              <Input
                value={newTag}
                onChange={(e) => setNewTag(e.target.value)}
                placeholder="Add a tag..."
                onKeyDown={(e) => e.key === 'Enter' && addTag()}
              />
              <Button type="button" size="sm" variant="outline" onClick={addTag}>Add</Button>
            </div>
            <div className="flex flex-wrap gap-2 mt-2">
              {availableTags
                .filter(tag => !filters.tags.includes(tag))
                .map((tag) => (
                  <Button
                    key={tag}
                    variant={filters.tags.includes(tag) ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => handleTagToggle(tag)}
                  >
                    {tag}
                  </Button>
                ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label className="flex items-center">
              <CalendarIcon className="h-3.5 w-3.5 mr-1.5" />
              Due Date Range
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant={"outline"}
                    className={cn(
                      "w-full justify-start text-left font-normal",
                      !filters.dueDateFrom && "text-muted-foreground"
                    )}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {filters.dueDateFrom ? format(new Date(filters.dueDateFrom), "PPP") : <span>Start date</span>}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={filters.dueDateFrom ? new Date(filters.dueDateFrom) : undefined}
                    onSelect={handleDueDateFromChange}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>

              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant={"outline"}
                    className={cn(
                      "w-full justify-start text-left font-normal",
                      !filters.dueDateTo && "text-muted-foreground"
                    )}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {filters.dueDateTo ? format(new Date(filters.dueDateTo), "PPP") : <span>End date</span>}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={filters.dueDateTo ? new Date(filters.dueDateTo) : undefined}
                    onSelect={handleDueDateToChange}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}