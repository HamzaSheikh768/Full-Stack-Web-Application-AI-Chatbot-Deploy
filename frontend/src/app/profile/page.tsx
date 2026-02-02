"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Calendar, Mail, MapPin, User, Settings, Shield, Bell, LogOut, Activity } from "lucide-react";
import { formatDate } from "@/lib/utils";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

export default function ProfilePage() {
  const [user, setUser] = useState<{ id: string; email: string; name?: string; } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading, user: authUser, logout } = useAuth();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/auth/login');
    } else if (isAuthenticated && authUser) {
      // Set the authenticated user data
      setUser(authUser);
      setIsLoading(false);
    }
  }, [isAuthenticated, authLoading, authUser, router]);

  if (isLoading || authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  const handleLogout = async () => {
    try {
      // Logout from the backend as well
      const token = localStorage.getItem('access_token');
      if (token) {
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        }).catch(() => {
          // If logout fails, continue with frontend logout anyway
        });
      }

      // Perform frontend logout
      await logout();
      router.push('/auth/login');
    } catch (error) {
      console.error('Logout error:', error);
      // Still redirect to login even if backend logout fails
      await logout();
      router.push('/auth/login');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white">Profile</h1>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Profile Info Card */}
          <div className="md:col-span-2">
            <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-glass-border shadow-glass">
              <CardHeader>
                <CardTitle>Personal Information</CardTitle>
                <CardDescription>Your account details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-4">
                  <Avatar className="h-20 w-20">
                    <AvatarFallback>
                      {user?.name?.charAt(0) || user?.email?.charAt(0) || "U"}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
                      {user?.name || "Anonymous User"}
                    </h2>
                    <p className="text-gray-600 dark:text-gray-300">{user?.email || "No email"}</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4">
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Name</h3>
                    <p className="text-gray-800 dark:text-white">{user?.name || "Not provided"}</p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Email</h3>
                    <p className="text-gray-800 dark:text-white">{user?.email || "No email"}</p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Account ID</h3>
                    <p className="font-mono text-xs text-gray-800 dark:text-white break-all">{user?.id || "No ID"}</p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Role</h3>
                    <Badge variant="secondary">User</Badge>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Session Status</h3>
                    <Badge variant={isAuthenticated ? "default" : "destructive"}>
                      {isAuthenticated ? "Active" : "Inactive"}
                    </Badge>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Last Login</h3>
                    <p className="text-gray-800 dark:text-white">Recent</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Session Management Card */}
            <Card className="mt-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-glass-border shadow-glass">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  Session Management
                </CardTitle>
                <CardDescription>Manage your current session</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Having issues with chat or authentication? Try refreshing your session by logging out and back in.
                  </p>
                  <Button
                    onClick={handleLogout}
                    variant="destructive"
                    className="w-full"
                  >
                    <LogOut className="mr-2 h-4 w-4" />
                    Sign Out
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Account Actions */}
          <div>
            <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-glass-border shadow-glass">
              <CardHeader>
                <CardTitle>Account Actions</CardTitle>
                <CardDescription>Manage your account</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <Mail className="mr-2 h-4 w-4" />
                  Change Email
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <User className="mr-2 h-4 w-4" />
                  Update Profile
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Shield className="mr-2 h-4 w-4" />
                  Security Settings
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Bell className="mr-2 h-4 w-4" />
                  Notification Preferences
                </Button>

                <div className="pt-4 mt-4 border-t border-gray-200 dark:border-gray-700">
                  <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Need Help?</h4>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">
                    If you're experiencing authentication issues with the chatbot, try signing out and back in.
                  </p>
                  <Button
                    variant="outline"
                    className="w-full justify-start"
                    onClick={() => {
                      // Force a page reload to clear any cached state
                      window.location.reload();
                    }}
                  >
                    <Activity className="mr-2 h-4 w-4" />
                    Refresh Session
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}