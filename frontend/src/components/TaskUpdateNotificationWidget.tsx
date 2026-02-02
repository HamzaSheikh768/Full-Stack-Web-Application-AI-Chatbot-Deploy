'use client';

import { useEffect, useState } from 'react';
import { toast } from 'sonner';

interface TaskUpdateNotificationWidgetProps {
  onTaskUpdate?: (updateType: string, taskData: any) => void;
  userId: string;
}

export default function TaskUpdateNotificationWidget({
  onTaskUpdate,
  userId
}: TaskUpdateNotificationWidgetProps) {
  const [notifications, setNotifications] = useState<any[]>([]);

  // This component would typically subscribe to real-time updates
  // For now, we'll simulate it by listening to a global event or using a state management solution
  useEffect(() => {
    // In a real implementation, this would connect to a WebSocket or SSE endpoint
    // to receive real-time updates when tasks are modified via AI Chat

    const handleTaskUpdate = (event: CustomEvent) => {
      const { updateType, taskData } = event.detail;

      // Add notification to our list
      const newNotification = {
        id: Date.now(),
        type: updateType,
        task: taskData,
        timestamp: new Date()
      };

      setNotifications(prev => [newNotification, ...prev.slice(0, 4)]); // Keep only last 5

      // Show toast notification
      showToast(updateType, taskData);

      // Call parent callback if provided
      if (onTaskUpdate) {
        onTaskUpdate(updateType, taskData);
      }
    };

    // Listen for custom events dispatched when tasks are updated via AI
    window.addEventListener('taskUpdate', handleTaskUpdate as EventListener);

    return () => {
      window.removeEventListener('taskUpdate', handleTaskUpdate as EventListener);
    };
  }, [onTaskUpdate]);

  const showToast = (updateType: string, taskData: any) => {
    let message = '';
    switch(updateType) {
      case 'created':
        message = `Task "${taskData.title}" has been created`;
        toast.success(message);
        break;
      case 'updated':
        message = `Task "${taskData.title}" has been updated`;
        toast.info(message);
        break;
      case 'completed':
        message = `Task "${taskData.title}" has been completed`;
        toast.success(message);
        break;
      case 'deleted':
        message = `Task "${taskData.title}" has been deleted`;
        toast.warning(message);
        break;
      default:
        message = `Task "${taskData.title}" has been updated`;
        toast.info(message);
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`p-3 rounded-md shadow-lg ${
            notification.type === 'created' || notification.type === 'completed'
              ? 'bg-green-100 text-green-800 border border-green-200'
              : notification.type === 'deleted'
                ? 'bg-yellow-100 text-yellow-800 border border-yellow-200'
                : 'bg-blue-100 text-blue-800 border border-blue-200'
          }`}
        >
          <div className="font-medium capitalize">{notification.type} Task:</div>
          <div className="text-sm">{notification.task.title}</div>
          <div className="text-xs opacity-70">
            {notification.timestamp.toLocaleTimeString()}
          </div>
        </div>
      ))}
    </div>
  );
}