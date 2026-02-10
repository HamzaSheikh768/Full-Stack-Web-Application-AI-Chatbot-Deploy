'use client';

import { useState } from 'react';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { DateTimePicker } from './DateTimePicker';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ReminderConfigProps {
  reminderEnabled: boolean;
  reminderTime: string; // ISO string format
  onReminderEnabledChange: (enabled: boolean) => void;
  onReminderTimeChange: (time: string) => void;
}

export function ReminderConfig({
  reminderEnabled,
  reminderTime,
  onReminderEnabledChange,
  onReminderTimeChange
}: ReminderConfigProps) {
  const [timeBeforeOptions] = useState([
    { value: '0', label: 'At the time' },
    { value: '5', label: '5 minutes before' },
    { value: '15', label: '15 minutes before' },
    { value: '30', label: '30 minutes before' },
    { value: '60', label: '1 hour before' },
    { value: '120', label: '2 hours before' },
    { value: '1440', label: '1 day before' },
  ]);

  const handleTimeBeforeChange = (minutesStr: string) => {
    if (!reminderTime) return;

    const minutes = parseInt(minutesStr, 10);
    const reminderDate = new Date(reminderTime);

    if (minutes > 0) {
      // Subtract minutes from the reminder time
      reminderDate.setMinutes(reminderDate.getMinutes() - minutes);
    }
    // If minutes is 0, set reminder to the same time as due date

    onReminderTimeChange(reminderDate.toISOString());
  };

  const getTimeBeforeValue = (): string => {
    if (!reminderTime) return '0';

    const reminderDate = new Date(reminderTime);
    // Calculate the difference from the due date
    // This is a simplified calculation - in a real app, you'd store the original due date
    // and calculate the difference between due date and reminder time
    return '0'; // Default to 0 for now
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Reminder Configuration</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="space-y-0.5">
            <Label htmlFor="reminder-toggle">Enable Reminder</Label>
            <p className="text-xs text-muted-foreground">
              Get notified before the task is due
            </p>
          </div>
          <Switch
            id="reminder-toggle"
            checked={reminderEnabled}
            onCheckedChange={onReminderEnabledChange}
          />
        </div>

        {reminderEnabled && (
          <div className="space-y-4">
            <div>
              <Label>Reminder Time</Label>
              <DateTimePicker
                value={reminderTime}
                onChange={onReminderTimeChange}
                placeholder="Select reminder date and time"
              />
            </div>

            <div>
              <Label>Notify me</Label>
              <Select value={getTimeBeforeValue()} onValueChange={handleTimeBeforeChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Select time before" />
                </SelectTrigger>
                <SelectContent>
                  {timeBeforeOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}