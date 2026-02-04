'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  name?: string;
  first_name?: string;
  last_name?: string;
  avatar?: string;
  image?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check for existing token on mount
    const storedToken = localStorage.getItem('access_token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      try {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error('Error parsing stored user data:', error);
        // Clear invalid data
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
      }
    }

    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
      }

      const data = await response.json();

      if (data.success && data.data) {
        const { access_token, user } = data.data;

        // Store token and user data
        localStorage.setItem('access_token', access_token);

        // The backend returns user data in a different structure
        // Create a normalized user object that matches our interface
        const normalizedUser = {
          id: user.user_id, // Map user_id from backend to id for frontend
          email: user.email,
          name: user.name || user.first_name // Use either name or first_name if available
        };

        localStorage.setItem('user', JSON.stringify(normalizedUser));
        localStorage.setItem('user_id', user.user_id); // For API calls

        setToken(access_token);
        setUser(normalizedUser);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (email: string, password: string, name?: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Signup failed');
      }

      const data = await response.json();

      if (data.success && data.data) {
        // Signup response contains user data in a different structure than login
        // Extract user_id to store temporarily before login
        const { user_id } = data.data;
        if (user_id) {
          localStorage.setItem('user_id', user_id);
        }

        // Auto-login after signup to get the proper token and user data
        await login(email, password);
      } else {
        throw new Error(data.message || 'Signup failed');
      }
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    // Clear stored data
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    localStorage.removeItem('user_id');

    setToken(null);
    setUser(null);
  };

  const isAuthenticated = !!token && !!user;

  const value = {
    user,
    token,
    isLoading,
    login,
    logout,
    signup,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};