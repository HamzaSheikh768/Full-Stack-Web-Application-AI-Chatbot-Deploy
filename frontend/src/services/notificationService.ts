/**
 * Notification Service for TaskAPP
 * Handles various types of notifications including email notifications for upcoming deadlines
 */

import { Task } from '@/lib/api';

// Interface for notification settings
export interface NotificationSettings {
  emailEnabled: boolean;
  emailHoursBefore: number; // Hours before deadline to send email
  browserEnabled: boolean;
  browserMinutesBefore: number; // Minutes before deadline to show browser notification
}

// Default notification settings
export const DEFAULT_NOTIFICATION_SETTINGS: NotificationSettings = {
  emailEnabled: true,
  emailHoursBefore: 24, // 24 hours before deadline
  browserEnabled: true,
  browserMinutesBefore: 60, // 60 minutes before deadline
};

// Interface for a notification
export interface Notification {
  id: string;
  taskId: string;
  taskTitle: string;
  type: 'email' | 'browser' | 'push';
  scheduledAt: Date;
  sentAt?: Date;
  delivered?: boolean;
  userId: string;
}

// Conflict resolution strategy enum
export enum ConflictResolutionStrategy {
  LAST_WRITE_WINS = 'last_write_wins',
  TIMESTAMP_BASED = 'timestamp_based',
  SERVER_AUTHORITATIVE = 'server_authoritative',
}

// Main notification service class
export class NotificationService {
  private static instance: NotificationService;
  private notifications: Map<string, Notification> = new Map();
  private timers: Map<string, NodeJS.Timeout> = new Map();

  private constructor() {}

  public static getInstance(): NotificationService {
    if (!NotificationService.instance) {
      NotificationService.instance = new NotificationService();
    }
    return NotificationService.instance;
  }

  /**
   * Schedule notifications for upcoming task deadlines
   */
  public scheduleNotificationsForTask(task: Task, userId: string): void {
    if (!task.due_date) {
      // No due date, nothing to schedule
      return;
    }

    const dueDate = new Date(task.due_date);

    // Schedule email notification
    if (DEFAULT_NOTIFICATION_SETTINGS.emailEnabled) {
      this.scheduleEmailNotification(task, userId, dueDate);
    }

    // Schedule browser notification
    if (DEFAULT_NOTIFICATION_SETTINGS.browserEnabled) {
      this.scheduleBrowserNotification(task, userId, dueDate);
    }
  }

  /**
   * Schedule email notification for a task
   */
  private scheduleEmailNotification(task: Task, userId: string, dueDate: Date): void {
    const notificationTime = new Date(dueDate);
    notificationTime.setHours(notificationTime.getHours() - DEFAULT_NOTIFICATION_SETTINGS.emailHoursBefore);

    if (notificationTime > new Date()) {
      // Only schedule if the notification time is in the future
      const notificationId = `${task.id}-email`;

      const notification: Notification = {
        id: notificationId,
        taskId: task.id,
        taskTitle: task.title,
        type: 'email',
        scheduledAt: notificationTime,
        userId,
      };

      this.notifications.set(notificationId, notification);

      const timer = setTimeout(() => {
        this.sendEmailNotification(notification);
      }, notificationTime.getTime() - Date.now());

      this.timers.set(notificationId, timer);
    }
  }

  /**
   * Schedule browser notification for a task
   */
  private scheduleBrowserNotification(task: Task, userId: string, dueDate: Date): void {
    const notificationTime = new Date(dueDate);
    notificationTime.setMinutes(notificationTime.getMinutes() - DEFAULT_NOTIFICATION_SETTINGS.browserMinutesBefore);

    if (notificationTime > new Date()) {
      // Only schedule if the notification time is in the future
      const notificationId = `${task.id}-browser`;

      const notification: Notification = {
        id: notificationId,
        taskId: task.id,
        taskTitle: task.title,
        type: 'browser',
        scheduledAt: notificationTime,
        userId,
      };

      this.notifications.set(notificationId, notification);

      const timer = setTimeout(() => {
        this.sendBrowserNotification(notification);
      }, notificationTime.getTime() - Date.now());

      this.timers.set(notificationId, timer);
    }
  }

  /**
   * Send email notification
   * This would typically call an API endpoint to send the actual email
   */
  private async sendEmailNotification(notification: Notification): Promise<void> {
    try {
      // Update notification status
      const existingNotification = this.notifications.get(notification.id);
      if (existingNotification) {
        existingNotification.sentAt = new Date();
        existingNotification.delivered = true;
        this.notifications.set(notification.id, existingNotification);
      }

      // In a real implementation, this would call an API endpoint to send the email
      console.log(`Sending email notification for task: ${notification.taskTitle}`);

      // Example API call (would be implemented on the backend):
      /*
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/notifications/email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId: notification.userId,
          taskId: notification.taskId,
          taskTitle: notification.taskTitle,
          scheduledAt: notification.scheduledAt,
        }),
      });
      */

    } catch (error) {
      console.error('Failed to send email notification:', error);
      // Update notification status as failed
      const existingNotification = this.notifications.get(notification.id);
      if (existingNotification) {
        existingNotification.sentAt = new Date();
        existingNotification.delivered = false;
        this.notifications.set(notification.id, existingNotification);
      }
    }
  }

  /**
   * Send browser notification
   */
  private sendBrowserNotification(notification: Notification): void {
    try {
      // Update notification status
      const existingNotification = this.notifications.get(notification.id);
      if (existingNotification) {
        existingNotification.sentAt = new Date();
        existingNotification.delivered = true;
        this.notifications.set(notification.id, existingNotification);
      }

      // Check if browser notifications are supported and permission is granted
      if ('Notification' in window) {
        if (Notification.permission === 'granted') {
          new Notification(`Task Deadline Approaching: ${notification.taskTitle}`, {
            body: `Your task "${notification.taskTitle}" is due soon.`,
            icon: '/favicon.ico',
            tag: notification.id,
          });
        } else if (Notification.permission !== 'denied') {
          // Request permission if not already denied
          Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
              new Notification(`Task Deadline Approaching: ${notification.taskTitle}`, {
                body: `Your task "${notification.taskTitle}" is due soon.`,
                icon: '/favicon.ico',
                tag: notification.id,
              });
            }
          });
        }
      }

      console.log(`Sending browser notification for task: ${notification.taskTitle}`);
    } catch (error) {
      console.error('Failed to send browser notification:', error);
      // Update notification status as failed
      const existingNotification = this.notifications.get(notification.id);
      if (existingNotification) {
        existingNotification.sentAt = new Date();
        existingNotification.delivered = false;
        this.notifications.set(notification.id, existingNotification);
      }
    }
  }

  /**
   * Cancel all notifications for a specific task
   */
  public cancelNotificationsForTask(taskId: string): void {
    const notificationIds = Array.from(this.notifications.keys()).filter(id =>
      id.startsWith(taskId + '-')
    );

    for (const notificationId of notificationIds) {
      const timer = this.timers.get(notificationId);
      if (timer) {
        clearTimeout(timer);
      }
      this.notifications.delete(notificationId);
      this.timers.delete(notificationId);
    }
  }

  /**
   * Get all scheduled notifications for a user
   */
  public getScheduledNotifications(userId: string): Notification[] {
    return Array.from(this.notifications.values()).filter(
      notification => notification.userId === userId
    );
  }

  /**
   * Get notifications for a specific task
   */
  public getNotificationsForTask(taskId: string): Notification[] {
    return Array.from(this.notifications.values()).filter(
      notification => notification.taskId === taskId
    );
  }

  /**
   * Clean up all timers when the service is destroyed
   */
  public destroy(): void {
    for (const timer of this.timers.values()) {
      clearTimeout(timer);
    }
    this.timers.clear();
    this.notifications.clear();
  }
}

// Initialize the notification service
export const notificationService = NotificationService.getInstance();