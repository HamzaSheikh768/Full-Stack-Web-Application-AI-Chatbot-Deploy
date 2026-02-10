'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Calendar } from '@/components/ui/calendar';
import { cn } from '@/lib/utils';
import { format } from 'date-fns';
import { CalendarIcon, Clock } from 'lucide-react';

interface DateTimePickerProps {
  value: string; // ISO string format
  onChange: (value: string) => void; // ISO string format
  placeholder?: string;
  label?: string;
  className?: string;
}

export function DateTimePicker({ 
  value, 
  onChange, 
  placeholder = "Select date and time",
  label,
  className = ""
}: DateTimePickerProps) {
  const [open, setOpen] = useState(false);
  const [time, setTime] = useState<string>(() => {
    if (value) {
      const date = new Date(value);
      return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
    }
    return '09:00';
  });

  const handleDateSelect = (date: Date | undefined) => {
    if (!date) return;

    // Parse the current time from the time input
    const [hours, minutes] = time.split(':').map(Number);
    
    // Set the selected date with the current time
    date.setHours(hours, minutes, 0, 0);
    
    onChange(date.toISOString());
  };

  const handleTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = e.target.value;
    setTime(newTime);

    // Update the full datetime value
    if (value) {
      const date = new Date(value);
      const [hours, minutes] = newTime.split(':').map(Number);
      date.setHours(hours, minutes, 0, 0);
      onChange(date.toISOString());
    } else {
      // If no date selected yet, use today's date with the selected time
      const today = new Date();
      const [hours, minutes] = newTime.split(':').map(Number);
      today.setHours(hours, minutes, 0, 0);
      onChange(today.toISOString());
    }
  };

  return (
    <div className={className}>
      {label && <label className="block text-sm font-medium mb-1">{label}</label>}
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            className={cn(
              "w-full justify-start text-left font-normal",
              !value && "text-muted-foreground"
            )}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {value ? format(new Date(value), "PPP HH:mm") : <span>{placeholder}</span>}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={value ? new Date(value) : undefined}
            onSelect={handleDateSelect}
            initialFocus
          />
          <div className="p-3 border-t border-border">
            <div className="flex items-center">
              <Clock className="h-4 w-4 mr-2" />
              <label htmlFor="time-input" className="text-sm font-medium mr-2">Time:</label>
              <Input
                id="time-input"
                type="time"
                value={time}
                onChange={handleTimeChange}
                className="w-24"
              />
            </div>
          </div>
        </PopoverContent>
      </Popover>
    </div>
  );
}