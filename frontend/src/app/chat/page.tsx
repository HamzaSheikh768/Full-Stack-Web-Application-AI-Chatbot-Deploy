'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import ChatWidget from '@/components/ChatWidget';
import { useAuth } from '@/contexts/AuthContext';

interface AuthData {
  isAuthenticated: boolean;
  userId: string;
  user?: {
    id: string;
    email: string;
    name?: string;
  };
}

export default function ChatPage() {
  const [auth, setAuth] = useState<AuthData>({
    isAuthenticated: false,
    userId: "",
    user: undefined
  });
  const router = useRouter();
  const { user, isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        // Redirect to login if not authenticated
        router.push('/auth/login');
        return;
      }

      if (user) {
        setAuth({
          isAuthenticated: true,
          userId: user.id,
          user: {
            id: user.id,
            email: user.email,
            name: user.name
          }
        });
      }
    }
  }, [isAuthenticated, isLoading, user, router]);



  return (
    <div className="min-h-screen bg-background pt-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 max-w-4xl">
        {/* Animated heading with underline */}
        <div className="mb-8 sm:mb-10 relative">
          <h1 className="text-2xl sm:text-3xl font-bold text-foreground inline-block relative group">
            AI Task Assistant
            <span className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 dark:bg-blue-400 scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></span>
          </h1>
        </div>

        <div className="mb-4 sm:mb-6">
          <p className="text-base sm:text-lg text-muted-foreground text-center max-w-2xl mx-auto">
            Manage your tasks using natural language
          </p>
        </div>

        {/* Main chat area without sidebar */}
        <div className="bg-card border border-border rounded-2xl shadow-sm hover:shadow-md transition-shadow duration-300">
          <div className="p-4 sm:p-6">
            <ChatWidget userId={auth.userId} />
          </div>
        </div>
      </div>
    </div>
  );
}