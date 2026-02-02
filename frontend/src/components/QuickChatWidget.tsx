'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { MessageSquare, X, Send } from 'lucide-react';
import { toast } from 'sonner';

interface QuickChatWidgetProps {
  userId: string;
}

export default function QuickChatWidget({ userId }: QuickChatWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || isLoading) return;

    setIsLoading(true);
    try {
      // Send message to chat API with authentication
      const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
      if (!token) {
        throw new Error('Authentication token not found');
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,  // Add JWT token for authentication
        },
        body: JSON.stringify({
          message: message.trim(),
          conversation_id: null // Start new conversation
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      toast.success('Message sent successfully!');
      setMessage(''); // Clear input after successful send
      // Optionally, we could display the response in the widget too
    } catch (error: any) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) {
    return (
      <Button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 rounded-full h-14 w-14 shadow-lg z-50 bg-blue-600 hover:bg-blue-700"
        aria-label="Open quick chat"
      >
        <MessageSquare className="h-6 w-6" />
      </Button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <Card className="w-80 shadow-xl border">
        <CardContent className="p-4">
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-semibold">AI Assistant</h3>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask to manage tasks..."
              className="flex-1 px-3 py-2 text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
            <Button
              type="submit"
              size="sm"
              disabled={isLoading || !message.trim()}
              aria-label="Send message"
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}