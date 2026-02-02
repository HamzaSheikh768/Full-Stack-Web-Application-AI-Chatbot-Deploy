'use client';

import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Mic, History } from 'lucide-react';
import { toast } from 'sonner';
import { useRouter } from 'next/navigation';
import { decodeToken, getStoredToken } from '@/lib/jwt-utils';

import VoiceInputWidget from './VoiceInputWidget';

interface ChatWidgetProps {
  userId: string;
  initialConversationId?: number;
}

interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  createdAt: Date;
}

interface Conversation {
  id: number;
  title: string;
  lastMessageAt: Date;
}

export default function ChatWidget({ userId, initialConversationId }: ChatWidgetProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(initialConversationId || null);
  const [showHistory, setShowHistory] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const router = useRouter();
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Load conversation history on component mount
  useEffect(() => {
    const loadConversationHistory = async () => {
      if (!conversationId) return;

      try {
        setIsLoading(true);

        // Fetch conversation history from API using the dedicated history endpoint
        const token = getStoredToken();
        if (!token) {
          throw new Error('Authentication token not found. Please log in again.');
        }

        // Use the utility function to get user ID from token to ensure consistency
        let tokenUserId = null;
        try {
          const payload = decodeToken(token);
          tokenUserId = payload.sub || payload.user_id; // Check both 'sub' and 'user_id' claims

          // Convert to string for comparison to handle different data types
          tokenUserId = String(tokenUserId);
        } catch (decodeError) {
          console.warn('Could not decode token to verify user ID:', decodeError);
          // Continue with request, let backend handle validation
          tokenUserId = null;
        }

        // Verify that the token user ID matches the component's user ID
        // Convert userId to string as well for comparison
        const stringUserId = String(userId);
        if (tokenUserId && tokenUserId !== stringUserId) {
          console.warn(`User ID mismatch in history load: token has '${tokenUserId}', component has '${stringUserId}'.`);
          // Show a more helpful error to the user
          toast.error('User ID mismatch detected. Please log out and log back in to refresh your session.');
          // Still proceed with the API call, let backend handle final validation
          // throw new Error('User ID mismatch. Access denied.');
        }

        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/api/${userId}/conversations/${conversationId}/history`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,  // Add JWT token for authentication
          },
        });

        if (!response.ok) {
          if (response.status === 403) {
            throw new Error('Access forbidden. Please check your permissions.');
          } else if (response.status === 401) {
            // Clear invalid token
            localStorage.removeItem('access_token');
            throw new Error('Unauthorized. Please log in again.');
          } else {
            throw new Error(`Failed to load conversation: ${response.status}`);
          }
        }

        const data = await response.json();

        // Convert API response to ChatMessage format
        const historyMessages: ChatMessage[] = data.messages.map((msg: any) => ({
          id: msg.id.toString(),
          content: msg.content,
          role: msg.role,
          createdAt: new Date(msg.created_at)
        }));

        setMessages(historyMessages);
      } catch (error: any) {
        console.error('Error loading conversation history:', error);

        // Specific error handling for different types of errors
        if (error.message.includes('Access forbidden') || error.message.includes('session may have expired')) {
          toast.error('Access forbidden. Your session may have expired. Please log in again.');
          // Optionally redirect to login
          // router.push('/auth/login');
        } else if (error.message.includes('Unauthorized')) {
          toast.error('Unauthorized access. Please log in again.');
          // Optionally redirect to login
          // router.push('/auth/login');
        } else {
          toast.error('Failed to load conversation history');
        }
      } finally {
        setIsLoading(false);
      }
    };

    if (conversationId) {
      loadConversationHistory();
    }
  }, [conversationId, userId]);

  // Load conversation list for history panel
  const loadConversationHistoryList = async () => {
    try {
      const token = getStoredToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/${userId}/conversations`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,  // Add JWT token for authentication
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to load conversations: ${response.status}`);
      }

      const data = await response.json();

      // Convert to Conversation interface
      const convList: Conversation[] = data.conversations.map((conv: any) => ({
        id: conv.id,
        title: conv.title || `Conversation ${conv.id}`,
        lastMessageAt: conv.last_message_at ? new Date(conv.last_message_at) : new Date(conv.updated_at)
      }));

      setConversations(convList);
    } catch (error: any) {
      console.error('Error loading conversation list:', error);
      toast.error('Failed to load conversation history list');
    }
  };

  // Toggle history panel
  const toggleHistory = () => {
    if (!showHistory) {
      loadConversationHistoryList();
    }
    setShowHistory(!showHistory);
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Load a specific conversation
  const loadConversation = (convId: number) => {
    setConversationId(convId);
    setMessages([]); // Clear current messages
    setShowHistory(false); // Close history panel
  };

  // Handle sending a message
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessageContent = inputValue.trim();
    setInputValue('');

    // Add user message to UI immediately
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      content: userMessageContent,
      role: 'user',
      createdAt: new Date()
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      setIsLoading(true);

      // Send to backend API with authentication
      const token = getStoredToken();
      if (!token) {
        throw new Error('Authentication token not found. Please log in again.');
      }

      // Use the utility function to get user ID from token to ensure consistency
      let tokenUserId = null;
      try {
        const payload = decodeToken(token);
        tokenUserId = payload.sub || payload.user_id; // Check both 'sub' and 'user_id' claims

        // Convert to string for comparison to handle different data types
        tokenUserId = String(tokenUserId);
      } catch (decodeError) {
        console.warn('Could not decode token to verify user ID:', decodeError);
        // Continue with request, let backend handle validation
        tokenUserId = null;
      }

      // Verify that the token user ID matches the component's user ID
      // Convert userId to string as well for comparison
      const stringUserId = String(userId);
      if (tokenUserId && tokenUserId !== stringUserId) {
        console.warn(`User ID mismatch: token has '${tokenUserId}', component has '${stringUserId}'.`);
        // Show a more helpful error to the user
        toast.error('User ID mismatch detected. Please log out and log back in to refresh your session.');
        // Still proceed with the API call, let backend handle final validation
        // throw new Error('User ID mismatch. Access denied.');
      }

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,  // Add JWT token for authentication
        },
        body: JSON.stringify({
          message: userMessageContent,
          conversation_id: conversationId || undefined
        })
      });

      if (!response.ok) {
        if (response.status === 403) {
          throw new Error('Access forbidden. Please check your permissions.');
        } else if (response.status === 401) {
          // Clear invalid token
          localStorage.removeItem('access_token');
          throw new Error('Unauthorized. Please log in again.');
        } else {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
      }

      const data = await response.json();

      // Update conversation ID if it's the first message
      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      // Add assistant response to UI
      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        role: 'assistant',
        createdAt: new Date()
      };

      setMessages(prev => [...prev, assistantMsg]);

      // Handle tool calls if any
      if (data.tool_calls && data.tool_calls.length > 0) {
        // Show tool call confirmations
        data.tool_calls.forEach((toolCall: any) => {
          const toolConfirmationMsg: ChatMessage = {
            id: (Date.now() + 2).toString(),
            content: `Tool "${toolCall.name}" executed successfully`,
            role: 'assistant',
            createdAt: new Date()
          };
          setMessages(prev => [...prev, toolConfirmationMsg]);
        });
      }
    } catch (error: any) {
      console.error('Chat error:', error);

      // Specific error handling for different types of errors
      if (error.message.includes('Access forbidden') || error.message.includes('session may have expired')) {
        toast.error('Access forbidden. Your session may have expired. Please log in again.');
        // Optionally redirect to login
        // router.push('/auth/login');
      } else if (error.message.includes('Unauthorized')) {
        toast.error('Unauthorized access. Please log in again.');
        // Optionally redirect to login
        // router.push('/auth/login');
      } else {
        toast.error('Failed to send message. Please try again.');
      }

      // Add error message to chat
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: error.message || 'Sorry, I encountered an error processing your request. Please try again.',
        role: 'assistant',
        createdAt: new Date()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto w-full">
      {/* History Panel */}
      {showHistory && (
        <div className="fixed inset-0 bg-white z-50 overflow-auto pt-16">  {/* Added top padding to account for navbar */}
          <div className="max-w-4xl mx-auto p-4">
            <div className="flex justify-between items-center mb-4 bg-white p-2 rounded-lg shadow-sm"> {/* Added bg and shadow to make header stand out */}
              <h2 className="text-xl font-bold">Conversation History</h2>
              <Button onClick={() => setShowHistory(false)} variant="outline" className="ml-4">
                Close
              </Button>
            </div>

            <div className="space-y-2 bg-white bg-opacity-90 backdrop-blur-sm rounded-lg p-3 shadow-md">
              {conversations.length > 0 ? (
                conversations.map(conv => (
                  <div
                    key={conv.id}
                    className="p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
                    onClick={() => loadConversation(conv.id)}
                  >
                    <div className="font-medium">{conv.title}</div>
                    <div className="text-sm text-gray-500">
                      Last message: {conv.lastMessageAt ? conv.lastMessageAt.toLocaleDateString() : 'N/A'}
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-center text-gray-500 py-4">No conversation history available</p>
              )}
            </div>
          </div>
        </div>
      )}

      {!showHistory && (
        <>
          <div className="flex-1 overflow-hidden">
            <div className="h-[60vh] overflow-y-auto p-4">
              <div className="flex justify-end mb-4">
                <Button onClick={toggleHistory} variant="outline" size="sm">
                  <History className="h-4 w-4 mr-2" />
                  History
                </Button>
              </div>

              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <h2 className="text-2xl font-bold mb-2">AI Task Assistant</h2>
                  <p className="text-muted-foreground mb-4">
                    How can I help you manage your tasks today?
                  </p>
                  <p className="text-sm text-muted-foreground">
                    You can speak or type commands like "Add a task to buy groceries" or "Show my tasks"
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg px-4 py-2 ${
                          msg.role === 'user'
                            ? 'bg-blue-600 text-white rounded-br-none'
                            : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-bl-none'
                        }`}
                      >
                        {msg.content}
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-lg px-4 py-2 rounded-bl-none">
                        <div className="flex items-center space-x-2">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div>
                            <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-100"></div>
                            <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-200"></div>
                          </div>
                          <span className="text-sm">AI is thinking...</span>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              )}
            </div>
          </div>

          <div className="border-t p-4">
            <form onSubmit={handleSendMessage} className="flex gap-2">
              <VoiceInputWidget
                onTranscript={(text) => setInputValue(text)}
                onError={(error) => toast.error(`Voice input error: ${error}`)}
              />

              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder={isLoading ? "Processing message..." : "Type your message or use voice input..."}
                disabled={isLoading}
                className="flex-1"
              />

              <Button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                size="icon"
              >
                {isLoading ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"></div>
                ) : (
                  <Send className="h-4 w-4" />
                )}
              </Button>
            </form>
          </div>
        </>
      )}
    </div>
  );
}